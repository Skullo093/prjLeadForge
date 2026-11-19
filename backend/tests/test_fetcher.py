import socket

import httpx
import pytest

from app.config import Settings
from app.services.site_analysis.fetcher import (
    HttpSiteFetcher,
    SiteInacessivel,
    normalizar_url,
    validar_destino,
)

HOSTS = {
    "publico.com": "93.184.216.34",
    "localhost": "127.0.0.1",
    "interno.local": "10.0.0.5",
    "metadados.local": "169.254.169.254",
    "v6.local": "::1",
}


def resolver_falso(host, porta, proto=0):
    if host not in HOSTS:
        raise socket.gaierror("não encontrado")
    familia = socket.AF_INET6 if ":" in HOSTS[host] else socket.AF_INET
    return [(familia, socket.SOCK_STREAM, 6, "", (HOSTS[host], porta))]


def _fetcher(handler, **configuracao):
    cfg = Settings(**{"site_timeout_segundos": 2, **configuracao})
    return HttpSiteFetcher(cfg, resolver=resolver_falso, transporte=httpx.MockTransport(handler))


def _html(texto="<html><body>oi</body></html>", tipo="text/html; charset=utf-8", status=200):
    return httpx.Response(status, text=texto, headers={"content-type": tipo})


def test_normalizar_url():
    assert normalizar_url("www.a.com") == "http://www.a.com"
    assert normalizar_url(" https://a.com ") == "https://a.com"


@pytest.mark.parametrize(
    "url",
    [
        "ftp://publico.com",
        "file:///etc/passwd",
        "http://localhost/admin",
        "http://interno.local/",
        "http://metadados.local/latest/meta-data",
        "http://v6.local/",
        "http://desconhecido.com/",
        "http:///sem-host",
    ],
)
def test_destinos_nao_permitidos(url):
    with pytest.raises(SiteInacessivel):
        validar_destino(url, resolver_falso)


def test_destino_publico_permitido():
    validar_destino("https://publico.com/pagina", resolver_falso)


def test_baixa_pagina_publica():
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        return _html()

    resultado = _fetcher(handler).buscar("publico.com")
    assert resultado.erro is None
    assert resultado.url_final == "http://publico.com"
    assert "oi" in resultado.html


def test_envia_user_agent_identificado():
    vistos = []

    def handler(request):
        vistos.append(request.headers["user-agent"])
        return _html() if request.url.path != "/robots.txt" else httpx.Response(404)

    _fetcher(handler).buscar("http://publico.com")
    assert vistos and all(agente.startswith("LeadForgeBot") for agente in vistos)


def test_respeita_robots_txt():
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nDisallow: /")
        return _html()

    resultado = _fetcher(handler).buscar("http://publico.com")
    assert resultado.html is None and "robots.txt" in resultado.erro


def test_bloqueia_redirecionamento_para_rede_interna():
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        return httpx.Response(302, headers={"location": "http://interno.local/segredo"})

    resultado = _fetcher(handler).buscar("http://publico.com")
    assert resultado.html is None and "não permitido" in resultado.erro


def test_segue_redirecionamento_para_https():
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        if request.url.scheme == "http":
            return httpx.Response(301, headers={"location": "https://publico.com/"})
        return _html()

    resultado = _fetcher(handler).buscar("http://publico.com")
    assert resultado.url_final == "https://publico.com/"


def test_limita_redirecionamentos():
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        return httpx.Response(302, headers={"location": "/outra"})

    assert "redirecionamentos" in _fetcher(handler).buscar("http://publico.com").erro


def test_rejeita_conteudo_que_nao_e_html_e_erros_http():
    def pdf(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        return httpx.Response(200, content=b"%PDF", headers={"content-type": "application/pdf"})

    def nao_encontrado(request):
        return httpx.Response(404)

    assert "HTML" in _fetcher(pdf).buscar("http://publico.com").erro
    assert "404" in _fetcher(nao_encontrado).buscar("http://publico.com").erro


def test_tempo_esgotado_e_falha_de_conexao():
    def lento(request):
        raise httpx.ReadTimeout("lento")

    def caido(request):
        raise httpx.ConnectError("caiu")

    assert _fetcher(lento).buscar("http://publico.com").erro == "tempo esgotado"
    assert _fetcher(caido).buscar("http://publico.com").erro == "falha de conexão"


def test_limita_tamanho_da_pagina():
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        return _html("a" * 50_000)

    resultado = _fetcher(handler, site_max_bytes=1000).buscar("http://publico.com")
    assert len(resultado.html) == 1000
