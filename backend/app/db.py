from collections.abc import Iterator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


def criar_engine(url: str) -> Engine:
    argumentos = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine = create_engine(url, connect_args=argumentos)
    if url.startswith("sqlite"):

        @event.listens_for(engine, "connect")
        def _ativar_chaves_estrangeiras(conexao, _registro):
            cursor = conexao.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


engine = criar_engine(get_settings().database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()


def get_fabrica_sessao() -> sessionmaker[Session]:
    """Fábrica de sessões para tarefas em segundo plano, que não reaproveitam a da requisição."""
    return SessionLocal
