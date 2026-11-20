from app.config import Settings
from app.services.discovery.base import EmpresaDescoberta, PlacesProvider, ProviderError
from app.services.discovery.demo import DemoPlacesProvider
from app.services.discovery.geoapify import GeoapifyProvider


def criar_provider(configuracao: Settings) -> PlacesProvider:
    if configuracao.modo_efetivo == "live":
        return GeoapifyProvider(configuracao)
    return DemoPlacesProvider()


__all__ = [
    "DemoPlacesProvider",
    "EmpresaDescoberta",
    "GeoapifyProvider",
    "PlacesProvider",
    "ProviderError",
    "criar_provider",
]
