"""Modelo de dados do LeadForge, derivado do diagrama de classes.

Acréscimos em relação ao diagrama: `Usuario` (login e isolamento por usuário, RNF-02),
`Busca` (acompanha o processamento assíncrono), `Evidencia.indica_problema` e o tipo de
evidência `DISPONIBILIDADE_SITE` (permite registrar "site não encontrado" como `desconhecido`).
"""

import enum
from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def agora() -> datetime:
    return datetime.now(UTC)


class NivelCerteza(enum.StrEnum):
    CONFIRMADO = "confirmado"
    SINAL_FORTE = "sinal_forte"
    INFERENCIA = "inferencia"
    DESCONHECIDO = "desconhecido"


class StatusContato(enum.StrEnum):
    NOVO = "novo"
    CONTATADO = "contatado"
    RESPONDEU = "respondeu"
    DESCARTADO = "descartado"


class TipoEvidencia(enum.StrEnum):
    DISPONIBILIDADE_SITE = "disponibilidade_site"
    HTTPS = "https"
    RESPONSIVIDADE_CELULAR = "responsividade_celular"
    BOTAO_WHATSAPP = "botao_whatsapp"
    FORMULARIO_CONTATO = "formulario_contato"
    CHAMADA_PARA_ACAO = "chamada_para_acao"


class StatusBusca(enum.StrEnum):
    PROCESSANDO = "processando"
    CONCLUIDA = "concluida"
    ERRO = "erro"
    CANCELADA = "cancelada"


def _enum(tipo: type[enum.Enum]) -> Enum:
    return Enum(tipo, values_callable=lambda e: [m.value for m in e], native_enum=False)


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(300))
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)

    perfil: Mapped["PerfilFreelancer"] = relationship(back_populates="usuario", uselist=False)


class PerfilFreelancer(Base):
    __tablename__ = "perfis_freelancer"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), unique=True)
    nome: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(254))
    habilidades: Mapped[list[str]] = mapped_column(JSON, default=list)
    servicos: Mapped[list[str]] = mapped_column(JSON, default=list)
    cidade: Mapped[str] = mapped_column(String(80), default="")
    estado: Mapped[str] = mapped_column(String(2), default="")
    tom_comunicacao: Mapped[str] = mapped_column(String(20), default="Amigável")

    usuario: Mapped[Usuario] = relationship(back_populates="perfil")


class Busca(Base):
    __tablename__ = "buscas"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    nicho: Mapped[str] = mapped_column(String(120))
    cidade: Mapped[str] = mapped_column(String(80))
    estado: Mapped[str] = mapped_column(String(2))
    limite: Mapped[int] = mapped_column(Integer)
    status: Mapped[StatusBusca] = mapped_column(_enum(StatusBusca), default=StatusBusca.PROCESSANDO)
    etapa: Mapped[str] = mapped_column(String(40), default="buscando_empresas")
    total_encontradas: Mapped[int] = mapped_column(Integer, default=0)
    novas: Mapped[int] = mapped_column(Integer, default=0)
    duplicadas: Mapped[int] = mapped_column(Integer, default=0)
    erro_codigo: Mapped[str | None] = mapped_column(String(40))
    erro_mensagem: Mapped[str | None] = mapped_column(String(300))
    criada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)
    concluida_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Empresa(Base):
    __tablename__ = "empresas"
    __table_args__ = (UniqueConstraint("usuario_id", "chave_dedup", name="uq_empresa_usuario"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    chave_dedup: Mapped[str] = mapped_column(String(300))
    nome: Mapped[str] = mapped_column(String(200))
    nicho: Mapped[str] = mapped_column(String(120))
    cidade: Mapped[str] = mapped_column(String(80))
    estado: Mapped[str] = mapped_column(String(2))
    bairro: Mapped[str | None] = mapped_column(String(120))
    endereco: Mapped[str | None] = mapped_column(String(300))
    telefone: Mapped[str | None] = mapped_column(String(40))
    url_site: Mapped[str | None] = mapped_column(String(500))
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)

    evidencias: Mapped[list["Evidencia"]] = relationship(
        back_populates="empresa", cascade="all, delete-orphan", order_by="Evidencia.id"
    )
    oportunidade: Mapped["Oportunidade"] = relationship(back_populates="empresa", uselist=False)


class Evidencia(Base):
    __tablename__ = "evidencias"

    id: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), index=True)
    tipo: Mapped[TipoEvidencia] = mapped_column(_enum(TipoEvidencia))
    valor: Mapped[str] = mapped_column(Text)
    nivel_certeza: Mapped[NivelCerteza] = mapped_column(_enum(NivelCerteza))
    origem_fonte: Mapped[str] = mapped_column(String(200))
    indica_problema: Mapped[bool] = mapped_column(Boolean, default=False)
    coletada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)

    empresa: Mapped[Empresa] = relationship(back_populates="evidencias")


class Oportunidade(Base):
    __tablename__ = "oportunidades"
    __table_args__ = (UniqueConstraint("usuario_id", "empresa_id", name="uq_oportunidade"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    busca_id: Mapped[int | None] = mapped_column(ForeignKey("buscas.id"))
    pontuacao: Mapped[int] = mapped_column(Integer, default=0)
    nivel_certeza: Mapped[NivelCerteza] = mapped_column(_enum(NivelCerteza))
    problemas: Mapped[list[str]] = mapped_column(JSON, default=list)
    status_contato: Mapped[StatusContato] = mapped_column(
        _enum(StatusContato), default=StatusContato.NOVO
    )
    criada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)

    empresa: Mapped[Empresa] = relationship(back_populates="oportunidade")
