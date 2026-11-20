import ipaddress
import socket
from dataclasses import dataclass
from typing import Protocol
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import httpx

from app.config import Settings

_MAX_REDIRECIONAMENTOS = 4


@dataclass(frozen=True)
class ResultadoSite:
    url_final: str | None
    html: str | None
    erro: str | None = None


class SiteFetcher(Protocol):
    def buscar(self, url: str) -> ResultadoSite: ...


class SiteInacessivel(Exception):
    pass


def normalizar_url(url: str) -> str:
    url = url.strip()
    return url if "://" in url else f"http://{url}"


def validar_destino(url: str, resolver=socket.getaddrinfo) -> None:
    """Bloqueia esquemas diferentes de http(s) e endereços que não sejam públicos (SSRF)."""
    partes = urlparse(url)
    if partes.scheme not in ("http", "https") or not partes.hostname:
        raise SiteInacessivel("endereço inválido")
    porta = partes.port or (443 if partes.scheme == "https" else 80)
    try:
        enderecos = resolver(partes.hostname, porta, proto=socket.IPPROTO_TCP)
    except OSError as erro:
        raise SiteInacessivel("endereço não encontrado") from erro
    for *_, destino in enderecos:
        if not ipaddress.ip_address(destino[0]).is_global:
            raise SiteInacessivel("endereço não permitido")


class HttpSiteFetcher:
    """Baixa o HTML público de um site, respeitando robots.txt e limites de tempo e tamanho."""

    def __init__(self, configuracao: Settings, resolver=socket.getaddrinfo, transporte=None):
        self._cfg = configuracao
        self._resolver = resolver
        self._cliente = httpx.Client(
            timeout=configuracao.site_timeout_segundos,
            follow_redirects=False,
            headers={"User-Agent": configuracao.site_user_agent},
            transport=transporte,
        )

    def buscar(self, url: str) -> ResultadoSite:
        try:
            url_final, html = self._baixar(normalizar_url(url))
        except SiteInacessivel as erro:
            return ResultadoSite(None, None, str(erro))
        except httpx.TimeoutException:
            return ResultadoSite(None, None, "tempo esgotado")
        except httpx.HTTPError:
            return ResultadoSite(None, None, "falha de conexão")
        return ResultadoSite(url_final, html)

    def _baixar(self, url: str) -> tuple[str, str]:
        for _ in range(_MAX_REDIRECIONAMENTOS + 1):
            validar_destino(url, self._resolver)
            if not self._robots_permite(url):
                raise SiteInacessivel("acesso bloqueado pelo robots.txt")
            with self._cliente.stream("GET", url) as resposta:
                if resposta.is_redirect:
                    destino = resposta.headers.get("location")
                    if not destino:
                        raise SiteInacessivel("redirecionamento inválido")
                    url = urljoin(url, destino)
                    continue
                if resposta.status_code >= 400:
                    raise SiteInacessivel(f"o site respondeu {resposta.status_code}")
                tipo = resposta.headers.get("content-type", "")
                if tipo and "html" not in tipo and "text" not in tipo:
                    raise SiteInacessivel("o conteúdo não é uma página HTML")
                corpo = b""
                for pedaco in resposta.iter_bytes():
                    corpo += pedaco
                    if len(corpo) >= self._cfg.site_max_bytes:
                        break
                codificacao = resposta.encoding or "utf-8"
            corpo = corpo[: self._cfg.site_max_bytes]
            return url, corpo.decode(codificacao, errors="replace")
        raise SiteInacessivel("redirecionamentos demais")

    def _robots_permite(self, url: str) -> bool:
        partes = urlparse(url)
        robots_url = f"{partes.scheme}://{partes.netloc}/robots.txt"
        try:
            validar_destino(robots_url, self._resolver)
            resposta = self._cliente.get(robots_url)
        except (SiteInacessivel, httpx.HTTPError):
            return True
        if resposta.status_code >= 400:
            return True
        analisador = RobotFileParser()
        analisador.parse(resposta.text.splitlines())
        return analisador.can_fetch(self._cfg.site_user_agent, url)
