from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class EmpresaDescoberta:
    nome: str
    cidade: str
    estado: str
    nicho: str
    external_id: str | None = None
    endereco: str | None = None
    bairro: str | None = None
    telefone: str | None = None
    url_site: str | None = None


class ProviderError(Exception):
    """Falha ao consultar a fonte de empresas, com código e mensagem prontos para o usuário."""

    def __init__(self, codigo: str, mensagem: str):
        super().__init__(mensagem)
        self.codigo = codigo
        self.mensagem = mensagem


class PlacesProvider(Protocol):
    def buscar(
        self, nicho: str, cidade: str, estado: str, limite: int
    ) -> list[EmpresaDescoberta]: ...
