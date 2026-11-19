from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.db import get_db, get_fabrica_sessao
from app.deps import usuario_atual
from app.models import Busca, Empresa, Oportunidade, StatusBusca, Usuario
from app.schemas import BuscaEntrada, BuscaSaida, ErroBuscaSaida, EtapaSaida, PreviaSaida
from app.services.busca_runner import ETAPAS, executar_busca
from app.services.discovery import PlacesProvider, criar_provider
from app.services.site_analysis.demo import DemoSiteFetcher
from app.services.site_analysis.fetcher import HttpSiteFetcher, SiteFetcher

router = APIRouter(prefix="/buscas", tags=["buscas"])


def get_provider(configuracao: Settings = Depends(get_settings)) -> PlacesProvider:
    return criar_provider(configuracao)


def get_fetcher(configuracao: Settings = Depends(get_settings)) -> SiteFetcher:
    return (
        HttpSiteFetcher(configuracao) if configuracao.modo_efetivo == "live" else DemoSiteFetcher()
    )


def _etapas(busca: Busca) -> list[EtapaSaida]:
    chaves = [chave for chave, _ in ETAPAS]
    posicao = chaves.index(busca.etapa) if busca.etapa in chaves else 0
    concluida = busca.status is StatusBusca.CONCLUIDA
    resultado = []
    for indice, (chave, rotulo) in enumerate(ETAPAS):
        if concluida or indice < posicao:
            estado = "concluida"
        elif indice == posicao and busca.status is StatusBusca.PROCESSANDO:
            estado = "ativa"
        else:
            estado = "pendente"
        resultado.append(EtapaSaida(chave=chave, rotulo=rotulo, estado=estado))
    return resultado


def _previa(db: Session, busca: Busca) -> list[PreviaSaida]:
    if busca.status is not StatusBusca.CONCLUIDA:
        return []
    linhas = db.execute(
        select(Oportunidade, Empresa)
        .join(Empresa, Empresa.id == Oportunidade.empresa_id)
        .where(Oportunidade.busca_id == busca.id, Oportunidade.usuario_id == busca.usuario_id)
        .order_by(Oportunidade.pontuacao.desc(), Oportunidade.id)
    ).all()
    return [
        PreviaSaida(
            oportunidade_id=oportunidade.id,
            empresa=empresa.nome,
            bairro=empresa.bairro,
            cidade=empresa.cidade,
            estado=empresa.estado,
            gargalo=oportunidade.problemas[0] if oportunidade.problemas else None,
            pontuacao=oportunidade.pontuacao,
        )
        for oportunidade, empresa in linhas
    ]


def _saida(db: Session, busca: Busca) -> BuscaSaida:
    erro = None
    if busca.status is StatusBusca.ERRO:
        erro = ErroBuscaSaida(
            codigo=busca.erro_codigo or "ERRO", mensagem=busca.erro_mensagem or ""
        )
    return BuscaSaida(
        id=busca.id,
        nicho=busca.nicho,
        cidade=busca.cidade,
        estado=busca.estado,
        limite=busca.limite,
        status=busca.status,
        etapas=_etapas(busca),
        total_encontradas=busca.total_encontradas,
        novas=busca.novas,
        duplicadas=busca.duplicadas,
        erro=erro,
        previa=_previa(db, busca),
    )


def _buscar_do_usuario(db: Session, busca_id: int, usuario: Usuario) -> Busca:
    busca = db.get(Busca, busca_id)
    if busca is None or busca.usuario_id != usuario.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Busca não encontrada.")
    return busca


@router.post("", response_model=BuscaSaida, status_code=status.HTTP_202_ACCEPTED)
def criar_busca(
    dados: BuscaEntrada,
    tarefas: BackgroundTasks,
    usuario: Usuario = Depends(usuario_atual),
    db: Session = Depends(get_db),
    provider: PlacesProvider = Depends(get_provider),
    fetcher: SiteFetcher = Depends(get_fetcher),
    fabrica_sessao=Depends(get_fabrica_sessao),
) -> BuscaSaida:
    busca = Busca(usuario_id=usuario.id, **dados.model_dump())
    db.add(busca)
    db.commit()
    tarefas.add_task(executar_busca, busca.id, fabrica_sessao, provider, fetcher)
    return _saida(db, busca)


@router.get("/{busca_id}", response_model=BuscaSaida)
def consultar_busca(
    busca_id: int, usuario: Usuario = Depends(usuario_atual), db: Session = Depends(get_db)
) -> BuscaSaida:
    busca = _buscar_do_usuario(db, busca_id, usuario)
    db.refresh(busca)
    return _saida(db, busca)


@router.post("/{busca_id}/cancelar", response_model=BuscaSaida)
def cancelar_busca(
    busca_id: int, usuario: Usuario = Depends(usuario_atual), db: Session = Depends(get_db)
) -> BuscaSaida:
    busca = _buscar_do_usuario(db, busca_id, usuario)
    if busca.status is StatusBusca.PROCESSANDO:
        busca.status = StatusBusca.CANCELADA
        db.commit()
    return _saida(db, busca)
