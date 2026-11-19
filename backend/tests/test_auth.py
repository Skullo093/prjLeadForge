from app.security import gerar_hash_senha, verificar_senha
from tests.conftest import criar_usuario

CADASTRO = {
    "nome": "Lucas Almeida",
    "email": "lucas@exemplo.com",
    "senha": "senha-forte-1",
    "aceite_lgpd": True,
}


def test_cadastro_cria_usuario_e_perfil(client):
    resposta = client.post("/auth/cadastro", json=CADASTRO)
    assert resposta.status_code == 201
    token = resposta.json()["token"]
    perfil = client.get("/perfil", headers={"Authorization": f"Bearer {token}"}).json()
    assert perfil["nome"] == "Lucas Almeida"
    assert perfil["email"] == "lucas@exemplo.com"


def test_cadastro_nao_guarda_senha_em_texto(client, fabrica):
    client.post("/auth/cadastro", json=CADASTRO)
    from app.models import Usuario

    with fabrica() as db:
        usuario = db.query(Usuario).one()
    assert "senha-forte-1" not in usuario.senha_hash
    assert usuario.senha_hash.startswith("scrypt$")


def test_email_duplicado_retorna_409(client):
    client.post("/auth/cadastro", json=CADASTRO)
    resposta = client.post("/auth/cadastro", json={**CADASTRO, "email": "LUCAS@exemplo.com"})
    assert resposta.status_code == 409


def test_cadastro_exige_aceite_lgpd_e_senha_minima(client):
    assert client.post("/auth/cadastro", json={**CADASTRO, "aceite_lgpd": False}).status_code == 422
    assert client.post("/auth/cadastro", json={**CADASTRO, "senha": "curta"}).status_code == 422
    assert client.post("/auth/cadastro", json={**CADASTRO, "email": "invalido"}).status_code == 422


def test_login_correto_e_incorreto(client):
    client.post("/auth/cadastro", json=CADASTRO)
    ok = client.post("/auth/login", json={"email": "lucas@exemplo.com", "senha": "senha-forte-1"})
    assert ok.status_code == 200 and ok.json()["token"]
    errada = client.post("/auth/login", json={"email": "lucas@exemplo.com", "senha": "outra-senha"})
    inexistente = client.post(
        "/auth/login", json={"email": "x@exemplo.com", "senha": "senha-forte-1"}
    )
    assert errada.status_code == inexistente.status_code == 401
    assert errada.json() == inexistente.json()


def test_rotas_protegidas_exigem_token(client):
    for caminho in ("/perfil", "/oportunidades", "/auth/eu"):
        assert client.get(caminho).status_code == 401
    assert client.get("/perfil", headers={"Authorization": "Bearer lixo"}).status_code == 401


def test_hash_de_senha():
    primeiro, segundo = gerar_hash_senha("abc12345"), gerar_hash_senha("abc12345")
    assert primeiro != segundo
    assert verificar_senha("abc12345", primeiro)
    assert not verificar_senha("errada", primeiro)
    assert not verificar_senha("abc12345", "formato-invalido")


def test_token_de_outro_usuario_nao_acessa_dados_alheios(client):
    a = criar_usuario(client, "a@exemplo.com", "Ana")
    b = criar_usuario(client, "b@exemplo.com", "Beto")
    assert client.get("/perfil", headers=a).json()["nome"] == "Ana"
    assert client.get("/perfil", headers=b).json()["nome"] == "Beto"
