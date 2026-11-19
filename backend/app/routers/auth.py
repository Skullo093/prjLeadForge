from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import usuario_atual
from app.models import PerfilFreelancer, Usuario
from app.schemas import CadastroEntrada, LoginEntrada, TokenSaida, UsuarioSaida
from app.security import criar_token, gerar_hash_senha, verificar_senha

router = APIRouter(prefix="/auth", tags=["autenticação"])

# hash válido usado para gastar o mesmo tempo quando o e-mail não existe
_HASH_FALSO = gerar_hash_senha("senha-inexistente")


@router.post("/cadastro", response_model=TokenSaida, status_code=status.HTTP_201_CREATED)
def cadastrar(dados: CadastroEntrada, db: Session = Depends(get_db)) -> TokenSaida:
    email = dados.email.lower()
    if db.scalar(select(Usuario).where(Usuario.email == email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Já existe uma conta com este e-mail.")
    usuario = Usuario(email=email, senha_hash=gerar_hash_senha(dados.senha))
    usuario.perfil = PerfilFreelancer(nome=dados.nome, email=email)
    db.add(usuario)
    db.commit()
    return TokenSaida(token=criar_token(usuario.id), usuario=UsuarioSaida.model_validate(usuario))


@router.post("/login", response_model=TokenSaida)
def entrar(dados: LoginEntrada, db: Session = Depends(get_db)) -> TokenSaida:
    usuario = db.scalar(select(Usuario).where(Usuario.email == dados.email.lower()))
    senha_ok = verificar_senha(dados.senha, usuario.senha_hash if usuario else _HASH_FALSO)
    if not usuario or not senha_ok:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "E-mail ou senha incorretos.")
    return TokenSaida(token=criar_token(usuario.id), usuario=UsuarioSaida.model_validate(usuario))


@router.get("/eu", response_model=UsuarioSaida)
def quem_sou_eu(usuario: Usuario = Depends(usuario_atual)) -> Usuario:
    return usuario
