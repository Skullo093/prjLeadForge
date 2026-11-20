import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.db import Base, criar_engine, get_db, get_fabrica_sessao
from app.main import app
from app.routers.buscas import get_fetcher, get_provider
from app.services.discovery.demo import DemoPlacesProvider
from app.services.site_analysis.demo import DemoSiteFetcher


@pytest.fixture
def fabrica(tmp_path):
    engine = criar_engine(f"sqlite:///{tmp_path / 'teste.db'}")
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    engine.dispose()


@pytest.fixture
def client(fabrica):
    def _db():
        with fabrica() as sessao:
            yield sessao

    app.dependency_overrides[get_db] = _db
    app.dependency_overrides[get_fabrica_sessao] = lambda: fabrica
    app.dependency_overrides[get_provider] = DemoPlacesProvider
    app.dependency_overrides[get_fetcher] = DemoSiteFetcher
    yield TestClient(app)
    app.dependency_overrides.clear()


def criar_usuario(
    client: TestClient, email: str = "lucas@exemplo.com", nome: str = "Lucas Almeida"
):
    """Cadastra um usuário e devolve os cabeçalhos de autenticação."""
    resposta = client.post(
        "/auth/cadastro",
        json={"nome": nome, "email": email, "senha": "senha-forte-1", "aceite_lgpd": True},
    )
    assert resposta.status_code == 201, resposta.text
    return {"Authorization": f"Bearer {resposta.json()['token']}"}


def rodar_busca(client: TestClient, cabecalhos, **extra):
    corpo = {"nicho": "clínicas de estética", "cidade": "Sorocaba", "estado": "SP", "limite": 10}
    corpo.update(extra)
    criada = client.post("/buscas", json=corpo, headers=cabecalhos)
    assert criada.status_code == 202, criada.text
    return client.get(f"/buscas/{criada.json()['id']}", headers=cabecalhos).json()
