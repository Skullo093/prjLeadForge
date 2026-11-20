from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import usuario_atual
from app.models import Empresa, NivelCerteza, Oportunidade, StatusContato, Usuario
from app.schemas import OportunidadeDetalhe, OportunidadeItem, OportunidadesSaida

router = APIRouter(prefix="/oportunidades", tags=["oportunidades"])


def _item(oportunidade: Oportunidade, posicao: int) -> dict:
    empresa = oportunidade.empresa
    return {
        "id": oportunidade.id,
        "posicao": posicao,
        "empresa": empresa.nome,
        "nicho": empresa.nicho,
        "cidade": empresa.cidade,
        "estado": empresa.estado,
        "pontuacao": oportunidade.pontuacao,
        "problemas": oportunidade.problemas,
        "nivel_certeza": oportunidade.nivel_certeza,
        "status_contato": oportunidade.status_contato,
    }


@router.get("", response_model=OportunidadesSaida)
def listar(
    q: str | None = Query(default=None, max_length=100),
    status_contato: StatusContato | None = None,
    nivel_certeza: NivelCerteza | None = None,
    usuario: Usuario = Depends(usuario_atual),
    db: Session = Depends(get_db),
) -> OportunidadesSaida:
    """Lista as oportunidades do usuário, da maior para a menor pontuação (RF-06).

    A posição no ranking considera toda a carteira, mesmo com filtros aplicados.
    """
    todas = db.scalars(
        select(Oportunidade)
        .join(Empresa, Empresa.id == Oportunidade.empresa_id)
        .where(Oportunidade.usuario_id == usuario.id)
        .order_by(Oportunidade.pontuacao.desc(), Oportunidade.id)
    ).all()
    itens = []
    for posicao, oportunidade in enumerate(todas, start=1):
        if status_contato and oportunidade.status_contato != status_contato:
            continue
        if nivel_certeza and oportunidade.nivel_certeza != nivel_certeza:
            continue
        if q and q.strip().casefold() not in oportunidade.empresa.nome.casefold():
            continue
        itens.append(OportunidadeItem(**_item(oportunidade, posicao)))
    return OportunidadesSaida(total=len(itens), itens=itens)


@router.get("/{oportunidade_id}", response_model=OportunidadeDetalhe)
def detalhar(
    oportunidade_id: int, usuario: Usuario = Depends(usuario_atual), db: Session = Depends(get_db)
) -> OportunidadeDetalhe:
    oportunidade = db.get(Oportunidade, oportunidade_id)
    if oportunidade is None or oportunidade.usuario_id != usuario.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Oportunidade não encontrada.")
    posicao = 1 + db.scalar(
        select(func.count())
        .select_from(Oportunidade)
        .where(
            Oportunidade.usuario_id == usuario.id,
            (Oportunidade.pontuacao > oportunidade.pontuacao)
            | (
                (Oportunidade.pontuacao == oportunidade.pontuacao)
                & (Oportunidade.id < oportunidade.id)
            ),
        )
    )
    empresa = oportunidade.empresa
    return OportunidadeDetalhe(
        **_item(oportunidade, posicao),
        bairro=empresa.bairro,
        endereco=empresa.endereco,
        telefone=empresa.telefone,
        url_site=empresa.url_site,
        evidencias=empresa.evidencias,
    )
