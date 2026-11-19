from tests.conftest import criar_usuario

PERFIL = {
    "nome": "Lucas Almeida",
    "email": "lucas@empresa.com.br",
    "habilidades": ["React", " Python ", "react", "", "WordPress", "UX"],
    "servicos": ["Criação de site", "Landing page"],
    "cidade": "Sorocaba",
    "estado": "sp",
    "tom_comunicacao": "Amigável",
}


def test_atualizar_perfil_normaliza_dados(client):
    cabecalhos = criar_usuario(client)
    resposta = client.put("/perfil", json=PERFIL, headers=cabecalhos)
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["habilidades"] == ["React", "Python", "WordPress", "UX"]
    assert dados["estado"] == "SP"
    assert client.get("/perfil", headers=cabecalhos).json() == dados


def test_perfil_valida_tom_e_uf(client):
    cabecalhos = criar_usuario(client)
    assert (
        client.put(
            "/perfil", json={**PERFIL, "tom_comunicacao": "Gritando"}, headers=cabecalhos
        ).status_code
        == 422
    )
    assert (
        client.put("/perfil", json={**PERFIL, "estado": "XX"}, headers=cabecalhos).status_code
        == 422
    )
    assert (
        client.put("/perfil", json={**PERFIL, "nome": "A"}, headers=cabecalhos).status_code == 422
    )


def test_perfis_sao_isolados_por_usuario(client):
    a = criar_usuario(client, "a@exemplo.com", "Ana")
    b = criar_usuario(client, "b@exemplo.com", "Beto")
    client.put("/perfil", json=PERFIL, headers=a)
    assert client.get("/perfil", headers=b).json()["habilidades"] == []
