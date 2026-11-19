import hashlib
import logging
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from contextlib import AbstractContextManager

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    Busca,
    Empresa,
    Evidencia,
    NivelCerteza,
    Oportunidade,
    StatusBusca,
    TipoEvidencia,
    agora,
)
from app.services.discovery.base import EmpresaDescoberta, PlacesProvider, ProviderError
from app.services.niches import normalizar
from app.services.scoring import avaliar
from app.services.site_analysis.analyzer import EvidenciaColetada, analisar_site
from app.services.site_analysis.fetcher import SiteFetcher

log = logging.getLogger(__name__)

ETAPAS = [
    ("buscando_empresas", "Buscando empresas"),
    ("removendo_duplicatas", "Removendo duplicatas"),
    ("analisando_sites", "Analisando sites"),
]
_TRABALHADORES = 4


class _Cancelada(Exception):
    pass


def chave_primaria(empresa: EmpresaDescoberta) -> str:
    if empresa.external_id:
        return f"id:{empresa.external_id}"
    return _chave_nome_endereco(empresa)


def _chave_nome_endereco(empresa: EmpresaDescoberta) -> str:
    base = f"{normalizar(empresa.nome)}|{normalizar(empresa.endereco)}"
    return "na:" + hashlib.sha1(base.encode()).hexdigest()  # noqa: S324 (apenas identificador)


def remover_duplicadas_internas(empresas: list[EmpresaDescoberta]) -> list[EmpresaDescoberta]:
    """Remove repetições dentro do mesmo resultado (mesmo id ou mesmo nome e endereço)."""
    vistas: set[str] = set()
    unicas = []
    for empresa in empresas:
        chaves = {chave_primaria(empresa), _chave_nome_endereco(empresa)}
        if chaves & vistas:
            continue
        vistas |= chaves
        unicas.append(empresa)
    return unicas


def executar_busca(
    busca_id: int,
    fabrica_sessao: Callable[[], AbstractContextManager[Session]],
    provider: PlacesProvider,
    fetcher: SiteFetcher,
) -> None:
    with fabrica_sessao() as db:
        busca = db.get(Busca, busca_id)
        if busca is None:
            return
        try:
            _processar(db, busca, provider, fetcher)
        except _Cancelada:
            log.info("busca %s cancelada", busca_id)
        except ProviderError as erro:
            _falhar(db, busca, erro.codigo, erro.mensagem)
        except Exception:
            log.exception("erro inesperado na busca %s", busca_id)
            db.rollback()
            _falhar(
                db, busca, "ERRO_INTERNO", "Não foi possível concluir a busca. Tente novamente."
            )


def _falhar(db: Session, busca: Busca, codigo: str, mensagem: str) -> None:
    busca.status = StatusBusca.ERRO
    busca.erro_codigo = codigo
    busca.erro_mensagem = mensagem
    busca.concluida_em = agora()
    db.commit()


def _verificar_cancelamento(db: Session, busca: Busca) -> None:
    db.refresh(busca)
    if busca.status is StatusBusca.CANCELADA:
        raise _Cancelada


def _definir_etapa(db: Session, busca: Busca, etapa: str) -> None:
    busca.etapa = etapa
    db.commit()


def _processar(db: Session, busca: Busca, provider: PlacesProvider, fetcher: SiteFetcher) -> None:
    descobertas = provider.buscar(busca.nicho, busca.cidade, busca.estado, busca.limite)
    _verificar_cancelamento(db, busca)

    _definir_etapa(db, busca, "removendo_duplicatas")
    unicas = remover_duplicadas_internas(descobertas)
    chaves = [chave_primaria(e) for e in unicas]
    existentes = set(
        db.scalars(
            select(Empresa.chave_dedup).where(
                Empresa.usuario_id == busca.usuario_id, Empresa.chave_dedup.in_(chaves)
            )
        )
    )
    novas = [e for e in unicas if chave_primaria(e) not in existentes]
    busca.total_encontradas = len(unicas)
    busca.duplicadas = len(unicas) - len(novas)
    busca.novas = len(novas)
    db.commit()
    _verificar_cancelamento(db, busca)

    _definir_etapa(db, busca, "analisando_sites")
    with ThreadPoolExecutor(max_workers=_TRABALHADORES) as pool:
        evidencias = list(pool.map(lambda e: _analisar(e, fetcher), novas))
    _verificar_cancelamento(db, busca)

    for descoberta, coletadas in zip(novas, evidencias, strict=True):
        _persistir(db, busca, descoberta, coletadas)
    busca.status = StatusBusca.CONCLUIDA
    busca.concluida_em = agora()
    db.commit()


def _analisar(empresa: EmpresaDescoberta, fetcher: SiteFetcher) -> list[EvidenciaColetada]:
    try:
        return analisar_site(empresa.url_site, fetcher)
    except Exception:
        log.exception("falha ao analisar o site de %s", empresa.nome)
        return _inacessivel(empresa)


def _inacessivel(empresa: EmpresaDescoberta) -> list[EvidenciaColetada]:
    return [
        EvidenciaColetada(
            TipoEvidencia.DISPONIBILIDADE_SITE,
            "Site inacessível (falha na análise)",
            NivelCerteza.DESCONHECIDO,
            f"Tentativa de acesso a {empresa.url_site}",
            True,
        )
    ]


def _persistir(
    db: Session, busca: Busca, descoberta: EmpresaDescoberta, coletadas: list[EvidenciaColetada]
) -> None:
    empresa = Empresa(
        usuario_id=busca.usuario_id,
        chave_dedup=chave_primaria(descoberta),
        nome=descoberta.nome,
        nicho=descoberta.nicho,
        cidade=descoberta.cidade,
        estado=descoberta.estado,
        bairro=descoberta.bairro,
        endereco=descoberta.endereco,
        telefone=descoberta.telefone,
        url_site=descoberta.url_site,
        evidencias=[
            Evidencia(
                tipo=e.tipo,
                valor=e.valor,
                nivel_certeza=e.nivel_certeza,
                origem_fonte=e.origem_fonte,
                indica_problema=e.indica_problema,
            )
            for e in coletadas
        ],
    )
    avaliacao = avaliar(coletadas)
    empresa.oportunidade = Oportunidade(
        usuario_id=busca.usuario_id,
        busca_id=busca.id,
        pontuacao=avaliacao.pontuacao,
        nivel_certeza=avaliacao.nivel_certeza,
        problemas=avaliacao.problemas,
    )
    db.add(empresa)
    db.commit()
