from app.services.busca_runner import chave_primaria, remover_duplicadas_internas
from app.services.discovery.base import EmpresaDescoberta
from app.services.niches import categorias_geoapify, chave_do_nicho, normalizar


def _empresa(nome, endereco=None, external_id=None):
    return EmpresaDescoberta(
        nome=nome,
        cidade="Sorocaba",
        estado="SP",
        nicho="x",
        endereco=endereco,
        external_id=external_id,
    )


def test_remove_duplicadas_por_id():
    empresas = [_empresa("A", external_id="1"), _empresa("A (cópia)", external_id="1")]
    assert len(remover_duplicadas_internas(empresas)) == 1


def test_remove_duplicadas_por_nome_e_endereco_com_ids_diferentes():
    empresas = [
        _empresa("Clínica Bela", "Rua A, 10", "1"),
        _empresa("CLINICA  bela", "rua a, 10", "2"),
        _empresa("Clínica Bela", "Rua B, 20", "3"),
    ]
    assert [e.external_id for e in remover_duplicadas_internas(empresas)] == ["1", "3"]


def test_filiais_com_enderecos_diferentes_sao_mantidas():
    empresas = [_empresa("Rede Fit", "Rua A, 1"), _empresa("Rede Fit", "Rua B, 2")]
    assert len(remover_duplicadas_internas(empresas)) == 2


def test_chave_primaria_usa_id_quando_existe():
    assert chave_primaria(_empresa("A", external_id="9")) == "id:9"
    assert chave_primaria(_empresa("A", "Rua")).startswith("na:")


def test_normalizar():
    assert normalizar("  Clínicas   de ESTÉTICA ") == "clinicas de estetica"
    assert normalizar(None) == ""


def test_nichos():
    assert chave_do_nicho("Clínicas de Estética") == "estetica"
    assert chave_do_nicho("dentistas") == "odontologia"
    assert chave_do_nicho("estúdio de pilates") == "academia"
    assert chave_do_nicho("oficina") is None
    assert categorias_geoapify("restaurantes") == ["catering.restaurant"]
    assert categorias_geoapify("oficina") is None
