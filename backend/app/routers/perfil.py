from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import usuario_atual
from app.models import PerfilFreelancer, Usuario
from app.schemas import PerfilEntrada, PerfilSaida

router = APIRouter(prefix="/perfil", tags=["perfil"])


@router.get("", response_model=PerfilSaida)
def obter_perfil(usuario: Usuario = Depends(usuario_atual)) -> PerfilFreelancer:
    return usuario.perfil


@router.put("", response_model=PerfilSaida)
def atualizar_perfil(
    dados: PerfilEntrada, usuario: Usuario = Depends(usuario_atual), db: Session = Depends(get_db)
) -> PerfilFreelancer:
    perfil = usuario.perfil
    for campo, valor in dados.model_dump().items():
        setattr(perfil, campo, valor)
    db.add(perfil)
    db.commit()
    return perfil
