import httpx
import pytest

from app.config import Settings
from app.services.discovery import ProviderError, criar_provider
from app.services.discovery.demo import DemoPlacesProvider
from app.services.discovery.geoapify import GeoapifyProvider

CIDADE_OK = {"results": [{"place_id": "cidade123", "city": "Sorocaba"}]}
LUGARES = {
    "features": [
        {
            "properties": {
                "name": "Clínica Exemplo",
                "place_id": "p1",
                "address_line2": "Rua A, 10 - Centro",
                "suburb": "Centro",
                "website": "https://exemplo.com.br",
                "contact": {"phone": "+55 15 3333-0000"},
            }
        },
        {"properties": {"place_id": "p2"}},
        {
            "properties": {
                "name": "Sem Site",
                "place_id": "p3",
                "datasource": {"raw": {"phone": "15 9999-0000"}},
            }
        },
    ]
}


def _provider(handler, **kwargs):
    cfg = Settings(geoapify_api_key="chave-teste")
    cliente = httpx.Client(transport=httpx.MockTransport(handler))
    return GeoapifyProvider(cfg, cliente, espera_segundos=0, **kwargs)


def _handler_ok(registro=None):
    def handler(request):
        if registro is not None:
            registro.append(request)
        if request.url.path.endswith("/geocode/search"):
            return httpx.Response(200, json=CIDADE_OK)
        return httpx.Response(200, json=LUGARES)

    return handler


def test_busca_converte_resultados_e_ignora_sem_nome():
    empresas = _provider(_handler_ok()).buscar("clínicas de estética", "Sorocaba", "SP", 10)
    assert [e.nome for e in empresas] == ["Clínica Exemplo", "Sem Site"]
    primeira = empresas[0]
    assert primeira.external_id == "p1"
    assert primeira.url_site == "https://exemplo.com.br"
    assert primeira.telefone == "+55 15 3333-0000"
    assert primeira.bairro == "Centro"
    assert empresas[1].url_site is None and empresas[1].telefone == "15 9999-0000"


def test_busca_envia_categorias_filtro_e_chave():
    registro = []
    _provider(_handler_ok(registro)).buscar("odontologia", "Sorocaba", "SP", 5)
    cidade, lugares = registro
    assert cidade.url.params["text"] == "Sorocaba, SP, Brasil"
    assert lugares.url.params["categories"] == "healthcare.dentist"
    assert lugares.url.params["filter"] == "place:cidade123"
    assert lugares.url.params["apiKey"] == "chave-teste"
    assert lugares.url.params["limit"] == "10"


def test_limite_corta_resultados():
    empresas = _provider(_handler_ok()).buscar("academias", "Sorocaba", "SP", 1)
    assert len(empresas) == 1


def test_nicho_nao_suportado():
    with pytest.raises(ProviderError) as erro:
        _provider(_handler_ok()).buscar("oficina mecânica", "Sorocaba", "SP", 5)
    assert erro.value.codigo == "NICHO_NAO_SUPORTADO"


def test_cidade_nao_encontrada():
    def handler(request):
        return httpx.Response(200, json={"results": []})

    with pytest.raises(ProviderError) as erro:
        _provider(handler).buscar("academias", "Xyz", "SP", 5)
    assert erro.value.codigo == "CIDADE_NAO_ENCONTRADA"


@pytest.mark.parametrize(
    ("status", "codigo"), [(429, "GEOAPIFY_429"), (401, "GEOAPIFY_AUTH"), (403, "GEOAPIFY_AUTH")]
)
def test_erros_de_api_viram_codigos(status, codigo):
    with pytest.raises(ProviderError) as erro:
        _provider(lambda r: httpx.Response(status)).buscar("academias", "Sorocaba", "SP", 5)
    assert erro.value.codigo == codigo


def test_tenta_de_novo_em_erro_5xx_e_depois_desiste():
    chamadas = []

    def handler(request):
        chamadas.append(1)
        return httpx.Response(503)

    with pytest.raises(ProviderError) as erro:
        _provider(handler).buscar("academias", "Sorocaba", "SP", 5)
    assert erro.value.codigo == "GEOAPIFY_503" and len(chamadas) == 3


def test_recupera_apos_falha_temporaria():
    chamadas = []

    def handler(request):
        chamadas.append(1)
        if len(chamadas) == 1:
            raise httpx.ConnectError("caiu")
        return _handler_ok()(request)

    empresas = _provider(handler).buscar("academias", "Sorocaba", "SP", 5)
    assert empresas


def test_falha_de_rede_persistente():
    def handler(request):
        raise httpx.ConnectError("caiu")

    with pytest.raises(ProviderError) as erro:
        _provider(handler).buscar("academias", "Sorocaba", "SP", 5)
    assert erro.value.codigo == "GEOAPIFY_INDISPONIVEL"


def test_modo_define_o_provider():
    assert isinstance(
        criar_provider(Settings(mode="demo", geoapify_api_key="x")), DemoPlacesProvider
    )
    assert isinstance(
        criar_provider(Settings(mode="auto", geoapify_api_key="")), DemoPlacesProvider
    )
    assert isinstance(criar_provider(Settings(mode="auto", geoapify_api_key="x")), GeoapifyProvider)
    assert isinstance(criar_provider(Settings(mode="live", geoapify_api_key="x")), GeoapifyProvider)
