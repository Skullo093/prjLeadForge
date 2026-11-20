from tests.conftest import criar_usuario, rodar_busca


def _listar(client, cabecalhos, **params):
    resposta = client.get("/oportunidades", params=params, headers=cabecalhos)
    assert resposta.status_code == 200
    return resposta.json()


def test_lista_ordenada_por_pontuacao_com_posicao(client):
    cabecalhos = criar_usuario(client)
    rodar_busca(client, cabecalhos)
    dados = _listar(client, cabecalhos)
    pontuacoes = [i["pontuacao"] for i in dados["itens"]]
    assert dados["total"] == 8
    assert pontuacoes == sorted(pontuacoes, reverse=True)
    assert [i["posicao"] for i in dados["itens"]] == list(range(1, 9))
    primeiro = dados["itens"][0]
    assert primeiro["empresa"] == "Clínica Bela Forma"
    assert primeiro["nivel_certeza"] in {"confirmado", "sinal_forte"}
    assert primeiro["status_contato"] == "novo"
    assert "Sem versão para celular" in primeiro["problemas"]


def test_filtros_por_nome_status_e_certeza(client):
    cabecalhos = criar_usuario(client)
    rodar_busca(client, cabecalhos)
    assert _listar(client, cabecalhos, q="bela")["total"] == 1
    assert _listar(client, cabecalhos, q="inexistente")["total"] == 0
    assert _listar(client, cabecalhos, status_contato="novo")["total"] == 8
    assert _listar(client, cabecalhos, status_contato="respondeu")["total"] == 0
    desconhecidos = _listar(client, cabecalhos, nivel_certeza="desconhecido")
    assert desconhecidos["total"] >= 1
    assert all(i["nivel_certeza"] == "desconhecido" for i in desconhecidos["itens"])
    # a posição continua sendo a do ranking geral
    assert desconhecidos["itens"][0]["posicao"] > 1


def test_filtro_invalido_retorna_422(client):
    cabecalhos = criar_usuario(client)
    assert client.get("/oportunidades?nivel_certeza=talvez", headers=cabecalhos).status_code == 422


def test_detalhe_mostra_evidencias_com_certeza(client):
    cabecalhos = criar_usuario(client)
    rodar_busca(client, cabecalhos)
    lista = _listar(client, cabecalhos)["itens"]
    bela = next(i for i in lista if i["empresa"] == "Clínica Bela Forma")
    detalhe = client.get(f"/oportunidades/{bela['id']}", headers=cabecalhos).json()
    tipos = {e["tipo"]: e for e in detalhe["evidencias"]}
    assert set(tipos) == {
        "https",
        "responsividade_celular",
        "botao_whatsapp",
        "formulario_contato",
        "chamada_para_acao",
    }
    assert tipos["https"]["nivel_certeza"] == "confirmado"
    assert tipos["responsividade_celular"]["nivel_certeza"] == "sinal_forte"
    assert tipos["chamada_para_acao"]["nivel_certeza"] == "inferencia"
    assert all(e["origem_fonte"] for e in detalhe["evidencias"])
    assert detalhe["posicao"] == bela["posicao"]


def test_empresa_sem_site_fica_como_desconhecido(client):
    cabecalhos = criar_usuario(client)
    rodar_busca(client, cabecalhos)
    lista = _listar(client, cabecalhos)["itens"]
    vita = next(i for i in lista if i["empresa"] == "Espaço Vita Estética")
    assert vita["nivel_certeza"] == "desconhecido"
    assert vita["problemas"] == ["Sem site encontrado"]
    detalhe = client.get(f"/oportunidades/{vita['id']}", headers=cabecalhos).json()
    assert [e["nivel_certeza"] for e in detalhe["evidencias"]] == ["desconhecido"]


def test_site_inacessivel_nao_vira_afirmacao(client):
    cabecalhos = criar_usuario(client)
    rodar_busca(client, cabecalhos)
    lista = _listar(client, cabecalhos)["itens"]
    pura = next(i for i in lista if i["empresa"] == "Estética Pura Pele")
    assert pura["problemas"] == ["Site inacessível"]
    assert pura["nivel_certeza"] == "desconhecido"


def test_oportunidades_sao_isoladas_por_usuario(client):
    a = criar_usuario(client, "a@exemplo.com", "Ana")
    b = criar_usuario(client, "b@exemplo.com", "Beto")
    rodar_busca(client, a)
    assert _listar(client, b)["total"] == 0
    id_de_a = _listar(client, a)["itens"][0]["id"]
    assert client.get(f"/oportunidades/{id_de_a}", headers=b).status_code == 404
    assert client.get("/oportunidades/9999", headers=a).status_code == 404
