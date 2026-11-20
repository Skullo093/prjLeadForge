from app.models import Busca, Empresa, StatusBusca
from app.services.busca_runner import executar_busca
from app.services.discovery.demo import DemoPlacesProvider
from app.services.site_analysis.demo import DemoSiteFetcher
from tests.conftest import criar_usuario, rodar_busca


def test_busca_completa_gera_oportunidades_ordenadas(client):
    cabecalhos = criar_usuario(client)
    busca = rodar_busca(client, cabecalhos)

    assert busca["status"] == "concluida"
    assert [e["estado"] for e in busca["etapas"]] == ["concluida"] * 3
    assert busca["total_encontradas"] == 8
    assert busca["novas"] == 8 and busca["duplicadas"] == 0
    pontuacoes = [p["pontuacao"] for p in busca["previa"]]
    assert len(pontuacoes) == 8
    assert pontuacoes == sorted(pontuacoes, reverse=True)
    assert busca["previa"][0]["empresa"] == "Clínica Bela Forma"


def test_limite_de_resultados_e_respeitado(client):
    busca = rodar_busca(client, criar_usuario(client), limite=3)
    assert busca["total_encontradas"] == 3 and len(busca["previa"]) == 3


def test_repetir_busca_nao_duplica_empresas(client, fabrica):
    cabecalhos = criar_usuario(client)
    rodar_busca(client, cabecalhos)
    segunda = rodar_busca(client, cabecalhos)

    assert segunda["total_encontradas"] == 8
    assert segunda["duplicadas"] == 8 and segunda["novas"] == 0
    assert segunda["previa"] == []
    with fabrica() as db:
        assert db.query(Empresa).count() == 8
    assert client.get("/oportunidades", headers=cabecalhos).json()["total"] == 8


def test_mesma_empresa_pode_existir_na_carteira_de_outro_usuario(client, fabrica):
    rodar_busca(client, criar_usuario(client, "a@exemplo.com", "Ana"))
    segunda = rodar_busca(client, criar_usuario(client, "b@exemplo.com", "Beto"))
    assert segunda["novas"] == 8 and segunda["duplicadas"] == 0
    with fabrica() as db:
        assert db.query(Empresa).count() == 16


def test_falha_do_provedor_vira_estado_de_erro(client):
    busca = rodar_busca(client, criar_usuario(client), cidade="Erro")
    assert busca["status"] == "erro"
    assert busca["erro"]["codigo"] == "PLACES_503"
    assert "indisponível" in busca["erro"]["mensagem"]
    assert busca["previa"] == []


def test_validacao_da_busca(client):
    cabecalhos = criar_usuario(client)
    base = {"nicho": "academias", "cidade": "Sorocaba", "estado": "SP", "limite": 10}
    assert (
        client.post("/buscas", json={**base, "estado": "ZZ"}, headers=cabecalhos).status_code == 422
    )
    assert client.post("/buscas", json={**base, "limite": 0}, headers=cabecalhos).status_code == 422
    assert (
        client.post("/buscas", json={**base, "limite": 31}, headers=cabecalhos).status_code == 422
    )
    assert client.post("/buscas", json={**base, "nicho": ""}, headers=cabecalhos).status_code == 422
    assert client.post("/buscas", json=base).status_code == 401


def test_busca_de_outro_usuario_retorna_404(client):
    a = criar_usuario(client, "a@exemplo.com", "Ana")
    b = criar_usuario(client, "b@exemplo.com", "Beto")
    busca = rodar_busca(client, a)
    assert client.get(f"/buscas/{busca['id']}", headers=b).status_code == 404
    assert client.post(f"/buscas/{busca['id']}/cancelar", headers=b).status_code == 404


def test_cancelar_busca_em_andamento(client, fabrica):
    cabecalhos = criar_usuario(client)
    with fabrica() as db:
        db.add(Busca(usuario_id=1, nicho="academias", cidade="Sorocaba", estado="SP", limite=5))
        db.commit()
    resposta = client.post("/buscas/1/cancelar", headers=cabecalhos)
    assert resposta.json()["status"] == "cancelada"
    # cancelar de novo não altera nada
    assert client.post("/buscas/1/cancelar", headers=cabecalhos).json()["status"] == "cancelada"


def test_busca_cancelada_nao_gera_oportunidades(client, fabrica):
    criar_usuario(client)
    with fabrica() as db:
        db.add(
            Busca(
                usuario_id=1,
                nicho="academias",
                cidade="Sorocaba",
                estado="SP",
                limite=5,
                status=StatusBusca.CANCELADA,
            )
        )
        db.commit()
    executar_busca(1, fabrica, DemoPlacesProvider(), DemoSiteFetcher())
    with fabrica() as db:
        assert db.query(Empresa).count() == 0
        assert db.get(Busca, 1).status is StatusBusca.CANCELADA


def test_outros_nichos_funcionam_no_modo_demo(client):
    cabecalhos = criar_usuario(client)
    odonto = rodar_busca(client, cabecalhos, nicho="odontologia")
    assert odonto["status"] == "concluida" and odonto["total_encontradas"] == 6
    generico = rodar_busca(client, cabecalhos, nicho="oficinas mecânicas", limite=4)
    assert generico["status"] == "concluida" and generico["total_encontradas"] == 4
