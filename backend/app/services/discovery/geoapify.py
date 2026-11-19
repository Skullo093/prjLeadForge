import time

import httpx

from app.config import Settings
from app.services.discovery.base import EmpresaDescoberta, ProviderError
from app.services.niches import categorias_geoapify

_NICHOS_SUPORTADOS = "clínicas de estética, odontologia, academias ou restaurantes"


class GeoapifyProvider:
    """Busca empresas por nicho e cidade usando a Places API do Geoapify."""

    def __init__(
        self,
        configuracao: Settings,
        cliente: httpx.Client | None = None,
        tentativas: int = 3,
        espera_segundos: float = 0.5,
    ):
        self._cfg = configuracao
        self._cliente = cliente or httpx.Client(timeout=configuracao.geoapify_timeout_segundos)
        self._tentativas = tentativas
        self._espera = espera_segundos

    def buscar(self, nicho: str, cidade: str, estado: str, limite: int) -> list[EmpresaDescoberta]:
        categorias = categorias_geoapify(nicho)
        if not categorias:
            raise ProviderError(
                "NICHO_NAO_SUPORTADO",
                f"Ainda não buscamos esse nicho. Tente {_NICHOS_SUPORTADOS}.",
            )
        place_id = self._resolver_cidade(cidade, estado)
        dados = self._get(
            self._cfg.geoapify_places_endpoint,
            {
                "categories": ",".join(categorias),
                "filter": f"place:{place_id}",
                "limit": min(limite * 2, 50),
                "lang": "pt",
            },
        )
        empresas: list[EmpresaDescoberta] = []
        for feature in dados.get("features", []):
            empresa = self._converter(feature.get("properties", {}), nicho, cidade, estado)
            if empresa:
                empresas.append(empresa)
        return empresas[:limite]

    def _resolver_cidade(self, cidade: str, estado: str) -> str:
        dados = self._get(
            self._cfg.geoapify_search_endpoint,
            {
                "text": f"{cidade}, {estado}, Brasil",
                "type": "city",
                "filter": "countrycode:br",
                "format": "json",
                "limit": 1,
                "lang": "pt",
            },
        )
        resultados = dados.get("results") or []
        if not resultados or not resultados[0].get("place_id"):
            raise ProviderError(
                "CIDADE_NAO_ENCONTRADA", "Não encontramos essa cidade. Confira o nome e a UF."
            )
        return resultados[0]["place_id"]

    def _get(self, url: str, parametros: dict) -> dict:
        parametros = {**parametros, "apiKey": self._cfg.geoapify_api_key}
        ultimo_erro = "GEOAPIFY_INDISPONIVEL"
        for tentativa in range(self._tentativas):
            try:
                resposta = self._cliente.get(url, params=parametros)
            except httpx.HTTPError:
                ultimo_erro = "GEOAPIFY_INDISPONIVEL"
            else:
                if resposta.status_code == 429:
                    raise ProviderError(
                        "GEOAPIFY_429",
                        "Limite de requisições do serviço de busca atingido. "
                        "Tente novamente em alguns minutos.",
                    )
                if resposta.status_code in (401, 403):
                    raise ProviderError("GEOAPIFY_AUTH", "A chave do serviço de busca é inválida.")
                if resposta.status_code < 400:
                    return resposta.json()
                if resposta.status_code < 500:
                    raise ProviderError(
                        f"GEOAPIFY_{resposta.status_code}", "O serviço de busca recusou a consulta."
                    )
                ultimo_erro = f"GEOAPIFY_{resposta.status_code}"
            if tentativa < self._tentativas - 1:
                time.sleep(self._espera * (tentativa + 1))
        raise ProviderError(ultimo_erro, "O serviço de busca está indisponível no momento.")

    @staticmethod
    def _converter(props: dict, nicho: str, cidade: str, estado: str) -> EmpresaDescoberta | None:
        nome = (props.get("name") or "").strip()
        if not nome:
            return None
        bruto = (props.get("datasource") or {}).get("raw") or {}
        contato = props.get("contact") or {}
        return EmpresaDescoberta(
            external_id=props.get("place_id"),
            nome=nome,
            nicho=nicho.strip(),
            cidade=cidade.strip(),
            estado=estado,
            endereco=props.get("address_line2") or props.get("formatted"),
            bairro=props.get("suburb") or props.get("district"),
            telefone=contato.get("phone") or props.get("phone") or bruto.get("phone"),
            url_site=props.get("website") or contato.get("website") or bruto.get("website"),
        )
