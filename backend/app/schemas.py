from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models import NivelCerteza, StatusBusca, StatusContato, TipoEvidencia

TOM_COMUNICACAO = ("Formal", "Amigável", "Direto")
UFS = "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split()


class Saida(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# --- autenticação ---------------------------------------------------------------------------
class CadastroEntrada(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)
    aceite_lgpd: bool

    @field_validator("nome")
    @classmethod
    def _limpar_nome(cls, valor: str) -> str:
        return valor.strip()

    @field_validator("aceite_lgpd")
    @classmethod
    def _exigir_aceite(cls, valor: bool) -> bool:
        if not valor:
            raise ValueError("É necessário aceitar o uso de dados públicos corporativos (LGPD).")
        return valor


class LoginEntrada(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=1, max_length=128)


class UsuarioSaida(Saida):
    id: int
    email: str


class TokenSaida(BaseModel):
    token: str
    usuario: UsuarioSaida


# --- perfil ---------------------------------------------------------------------------------
def _limpar_lista(valores: list[str]) -> list[str]:
    vistos: dict[str, str] = {}
    for valor in valores:
        limpo = valor.strip()
        if limpo:
            vistos.setdefault(limpo.casefold(), limpo)
    return list(vistos.values())


class PerfilEntrada(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    email: EmailStr
    habilidades: list[str] = Field(default_factory=list, max_length=30)
    servicos: list[str] = Field(default_factory=list, max_length=20)
    cidade: str = Field(default="", max_length=80)
    estado: str = Field(default="", max_length=2)
    tom_comunicacao: Literal["Formal", "Amigável", "Direto"] = "Amigável"

    @field_validator("habilidades", "servicos")
    @classmethod
    def _normalizar_listas(cls, valores: list[str]) -> list[str]:
        return _limpar_lista([v[:60] for v in valores])

    @field_validator("estado")
    @classmethod
    def _validar_uf(cls, valor: str) -> str:
        valor = valor.strip().upper()
        if valor and valor not in UFS:
            raise ValueError("Informe uma UF válida.")
        return valor

    @field_validator("nome", "cidade")
    @classmethod
    def _aparar(cls, valor: str) -> str:
        return valor.strip()


class PerfilSaida(Saida):
    nome: str
    email: str
    habilidades: list[str]
    servicos: list[str]
    cidade: str
    estado: str
    tom_comunicacao: str


# --- buscas ---------------------------------------------------------------------------------
class BuscaEntrada(BaseModel):
    nicho: str = Field(min_length=2, max_length=120)
    cidade: str = Field(min_length=2, max_length=80)
    estado: str = Field(min_length=2, max_length=2)
    limite: int = Field(default=10, ge=1, le=30)

    @field_validator("nicho", "cidade")
    @classmethod
    def _aparar(cls, valor: str) -> str:
        return valor.strip()

    @field_validator("estado")
    @classmethod
    def _validar_uf(cls, valor: str) -> str:
        valor = valor.strip().upper()
        if valor not in UFS:
            raise ValueError("Informe uma UF válida.")
        return valor


class EtapaSaida(BaseModel):
    chave: str
    rotulo: str
    estado: Literal["concluida", "ativa", "pendente"]


class ErroBuscaSaida(BaseModel):
    codigo: str
    mensagem: str


class PreviaSaida(BaseModel):
    oportunidade_id: int
    empresa: str
    bairro: str | None
    cidade: str
    estado: str
    gargalo: str | None
    pontuacao: int


class BuscaSaida(BaseModel):
    id: int
    nicho: str
    cidade: str
    estado: str
    limite: int
    status: StatusBusca
    etapas: list[EtapaSaida]
    total_encontradas: int
    novas: int
    duplicadas: int
    erro: ErroBuscaSaida | None = None
    previa: list[PreviaSaida] = []


# --- oportunidades --------------------------------------------------------------------------
class EvidenciaSaida(Saida):
    tipo: TipoEvidencia
    valor: str
    nivel_certeza: NivelCerteza
    origem_fonte: str
    indica_problema: bool
    coletada_em: datetime


class OportunidadeItem(BaseModel):
    id: int
    posicao: int
    empresa: str
    nicho: str
    cidade: str
    estado: str
    pontuacao: int
    problemas: list[str]
    nivel_certeza: NivelCerteza
    status_contato: StatusContato


class OportunidadesSaida(BaseModel):
    total: int
    itens: list[OportunidadeItem]


class OportunidadeDetalhe(OportunidadeItem):
    bairro: str | None
    endereco: str | None
    telefone: str | None
    url_site: str | None
    evidencias: list[EvidenciaSaida]
