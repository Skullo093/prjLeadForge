from urllib.parse import parse_qs, urlparse

from app.services.discovery.demo import PADROES
from app.services.site_analysis.fetcher import ResultadoSite


def montar_html(https: bool, viewport: bool, whatsapp: bool, formulario: bool, cta: bool) -> str:
    cabecalho = (
        '<meta name="viewport" content="width=device-width, initial-scale=1">' if viewport else ""
    )
    partes = ["<h1>Bem-vindo</h1><p>Cuidamos de você com atenção.</p>"]
    if whatsapp:
        partes.append('<a href="https://wa.me/5515999990000">Fale pelo WhatsApp</a>')
    if formulario:
        partes.append(
            '<form><input type="text" name="nome"><input type="email" name="email">'
            '<textarea name="mensagem"></textarea></form>'
        )
    if cta:
        partes.append('<a href="/agendar" class="botao">Agende sua avaliação</a>')
    return f"<html><head><title>Site</title>{cabecalho}</head><body>{''.join(partes)}</body></html>"


class DemoSiteFetcher:
    """Devolve HTML simulado conforme o padrão (`?p=N`) gravado na URL da empresa demo."""

    def buscar(self, url: str) -> ResultadoSite:
        consulta = parse_qs(urlparse(url).query)
        try:
            padrao = PADROES[int(consulta["p"][0])]
        except (KeyError, ValueError, IndexError):
            return ResultadoSite(None, None, "site de demonstração desconhecido")
        if not isinstance(padrao, tuple):
            return ResultadoSite(None, None, "tempo esgotado")
        return ResultadoSite(url, montar_html(*padrao))
