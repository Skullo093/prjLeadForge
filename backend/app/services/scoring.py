"""Pontuação e ranqueamento (RF-06).

A pontuação soma o peso de cada problema detectado, reduzido conforme o nível de certeza da
evidência (um sinal menos certo vale menos). O resultado é limitado a 100.
"""

from dataclasses import dataclass

from app.models import NivelCerteza, TipoEvidencia
from app.services.site_analysis.analyzer import EvidenciaColetada

PESO_PROBLEMA: dict[TipoEvidencia, int] = {
    TipoEvidencia.DISPONIBILIDADE_SITE: 80,
    TipoEvidencia.RESPONSIVIDADE_CELULAR: 35,
    TipoEvidencia.HTTPS: 25,
    TipoEvidencia.BOTAO_WHATSAPP: 20,
    TipoEvidencia.FORMULARIO_CONTATO: 15,
    TipoEvidencia.CHAMADA_PARA_ACAO: 10,
}
MULTIPLICADOR_CERTEZA: dict[NivelCerteza, float] = {
    NivelCerteza.CONFIRMADO: 1.0,
    NivelCerteza.SINAL_FORTE: 0.85,
    NivelCerteza.INFERENCIA: 0.6,
    NivelCerteza.DESCONHECIDO: 0.8,
}
ROTULO_PROBLEMA: dict[TipoEvidencia, str] = {
    TipoEvidencia.DISPONIBILIDADE_SITE: "Sem site encontrado",
    TipoEvidencia.RESPONSIVIDADE_CELULAR: "Sem versão para celular",
    TipoEvidencia.HTTPS: "Site não seguro (sem HTTPS)",
    TipoEvidencia.BOTAO_WHATSAPP: "Sem botão de WhatsApp",
    TipoEvidencia.FORMULARIO_CONTATO: "Sem formulário de contato",
    TipoEvidencia.CHAMADA_PARA_ACAO: "Sem chamada para ação clara",
}


@dataclass(frozen=True)
class Avaliacao:
    pontuacao: int
    nivel_certeza: NivelCerteza
    problemas: list[str]


def _contribuicao(evidencia: EvidenciaColetada) -> float:
    peso = PESO_PROBLEMA[evidencia.tipo]
    if evidencia.tipo is TipoEvidencia.DISPONIBILIDADE_SITE and "inacessível" in evidencia.valor:
        peso = 40
    return peso * MULTIPLICADOR_CERTEZA[evidencia.nivel_certeza]


def avaliar(evidencias: list[EvidenciaColetada]) -> Avaliacao:
    problemas = sorted(
        (e for e in evidencias if e.indica_problema), key=_contribuicao, reverse=True
    )
    if not problemas:
        return Avaliacao(0, NivelCerteza.CONFIRMADO, [])
    pontuacao = min(100, int(sum(_contribuicao(e) for e in problemas) + 0.5))
    rotulos = []
    for problema in problemas:
        rotulo = ROTULO_PROBLEMA[problema.tipo]
        if problema.tipo is TipoEvidencia.DISPONIBILIDADE_SITE and "inacessível" in problema.valor:
            rotulo = "Site inacessível"
        rotulos.append(rotulo)
    return Avaliacao(pontuacao, problemas[0].nivel_certeza, rotulos)
