import re
from dataclasses import dataclass
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from app.models import NivelCerteza, TipoEvidencia
from app.services.niches import normalizar
from app.services.site_analysis.fetcher import ResultadoSite, SiteFetcher

FONTE_EMPRESA = "Dados da empresa (API de lugares)"
_REGEX_WHATSAPP = re.compile(r"(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com|^whatsapp:)", re.I)
_PALAVRAS_CTA = (
    "agende",
    "agendar",
    "orcamento",
    "solicite",
    "fale conosco",
    "fale com",
    "entre em contato",
    "contato",
    "reserve",
    "marque",
    "matricule",
    "peca",
    "compre",
    "whatsapp",
)
_CAMPOS_IGNORADOS = {"hidden", "search", "submit", "button", "reset", "image", "checkbox", "radio"}


@dataclass(frozen=True)
class EvidenciaColetada:
    tipo: TipoEvidencia
    valor: str
    nivel_certeza: NivelCerteza
    origem_fonte: str
    indica_problema: bool


@dataclass(frozen=True)
class SinaisHtml:
    viewport: bool
    whatsapp: bool
    formulario: bool
    cta: bool


def extrair_sinais(html: str) -> SinaisHtml:
    sopa = BeautifulSoup(html, "html.parser")
    viewport = sopa.find("meta", attrs={"name": re.compile("^viewport$", re.I)}) is not None
    whatsapp = any(_REGEX_WHATSAPP.search(a["href"]) for a in sopa.find_all("a", href=True))
    formulario = False
    for form in sopa.find_all("form"):
        if form.get("role") == "search":
            continue
        campos = [
            c
            for c in form.find_all(["input", "textarea", "select"])
            if c.name != "input" or (c.get("type") or "text").lower() not in _CAMPOS_IGNORADOS
        ]
        if campos:
            formulario = True
            break
    textos = [t.get_text(" ", strip=True) for t in sopa.find_all(["a", "button"])]
    textos += [i.get("value", "") for i in sopa.find_all("input", attrs={"type": "submit"})]
    cta = any(p in normalizar(t) for t in textos for p in _PALAVRAS_CTA)
    return SinaisHtml(viewport=viewport, whatsapp=whatsapp, formulario=formulario, cta=cta)


def analisar_site(url: str | None, fetcher: SiteFetcher) -> list[EvidenciaColetada]:
    """Transforma o site da empresa em evidências, cada uma com seu nível de certeza.

    Ausência de dado nunca vira afirmação: sem site ou site inacessível => `desconhecido`.
    """
    if not url:
        return [
            EvidenciaColetada(
                TipoEvidencia.DISPONIBILIDADE_SITE,
                "Site não encontrado",
                NivelCerteza.DESCONHECIDO,
                FONTE_EMPRESA,
                True,
            )
        ]
    resultado: ResultadoSite = fetcher.buscar(url)
    if resultado.html is None or resultado.url_final is None:
        return [
            EvidenciaColetada(
                TipoEvidencia.DISPONIBILIDADE_SITE,
                f"Site inacessível ({resultado.erro or 'motivo desconhecido'})",
                NivelCerteza.DESCONHECIDO,
                f"Tentativa de acesso a {urlparse(url).netloc or url}",
                True,
            )
        ]

    fonte = f"Análise do HTML de {urlparse(resultado.url_final).netloc}"
    sinais = extrair_sinais(resultado.html)
    https = urlparse(resultado.url_final).scheme == "https"
    conf, sinal, infer = NivelCerteza.CONFIRMADO, NivelCerteza.SINAL_FORTE, NivelCerteza.INFERENCIA

    def ev(tipo, ok, texto_ok, texto_falta, nivel_ok, nivel_falta):
        return EvidenciaColetada(
            tipo, texto_ok if ok else texto_falta, nivel_ok if ok else nivel_falta, fonte, not ok
        )

    return [
        ev(
            TipoEvidencia.HTTPS,
            https,
            "Site com HTTPS",
            "Site sem HTTPS (conexão não segura)",
            conf,
            conf,
        ),
        ev(
            TipoEvidencia.RESPONSIVIDADE_CELULAR,
            sinais.viewport,
            "Viewport configurado para celular",
            "Sem versão para celular (viewport ausente)",
            conf,
            sinal,
        ),
        ev(
            TipoEvidencia.BOTAO_WHATSAPP,
            sinais.whatsapp,
            "Link de WhatsApp encontrado",
            "Botão de WhatsApp não encontrado",
            conf,
            sinal,
        ),
        ev(
            TipoEvidencia.FORMULARIO_CONTATO,
            sinais.formulario,
            "Formulário de contato encontrado",
            "Formulário de contato não encontrado",
            conf,
            sinal,
        ),
        ev(
            TipoEvidencia.CHAMADA_PARA_ACAO,
            sinais.cta,
            "Chamada para ação identificada",
            "Sem chamada para ação clara",
            infer,
            infer,
        ),
    ]
