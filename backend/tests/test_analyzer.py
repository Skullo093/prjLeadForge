from app.models import NivelCerteza, TipoEvidencia
from app.services.site_analysis.analyzer import analisar_site, extrair_sinais
from app.services.site_analysis.fetcher import ResultadoSite

HTML_COMPLETO = """
<html><head><meta name="VIEWPORT" content="width=device-width"></head><body>
<a href="https://wa.me/5515999990000">Fale conosco</a>
<form><input name="nome"><textarea name="msg"></textarea></form>
<a href="/agendar">Agende sua consulta</a>
</body></html>
"""


class SiteFalso:
    def __init__(self, resultado):
        self.resultado = resultado

    def buscar(self, url):
        return self.resultado


def _por_tipo(evidencias):
    return {e.tipo: e for e in evidencias}


def test_extrair_sinais_detecta_tudo():
    sinais = extrair_sinais(HTML_COMPLETO)
    assert sinais.viewport and sinais.whatsapp and sinais.formulario and sinais.cta


def test_extrair_sinais_em_pagina_vazia():
    sinais = extrair_sinais("<html><body><p>Olá</p></body></html>")
    assert not (sinais.viewport or sinais.whatsapp or sinais.formulario or sinais.cta)


def test_busca_nao_conta_como_formulario_de_contato():
    html = '<form role="search"><input name="q"></form><form><input type="hidden" name="t"></form>'
    assert not extrair_sinais(html).formulario


def test_whatsapp_por_diferentes_links():
    for href in ("https://api.whatsapp.com/send?phone=1", "whatsapp://send?phone=1"):
        assert extrair_sinais(f'<a href="{href}">x</a>').whatsapp


def test_site_completo_sem_problemas():
    evidencias = analisar_site(
        "https://a.com", SiteFalso(ResultadoSite("https://a.com", HTML_COMPLETO))
    )
    assert len(evidencias) == 5
    assert not any(e.indica_problema for e in evidencias)
    assert all("a.com" in e.origem_fonte for e in evidencias)


def test_site_pobre_gera_problemas_com_certeza_correta():
    resultado = ResultadoSite("http://a.com", "<html><body>oi</body></html>")
    evidencias = _por_tipo(analisar_site("http://a.com", SiteFalso(resultado)))
    https = evidencias[TipoEvidencia.HTTPS]
    assert https.indica_problema and https.nivel_certeza is NivelCerteza.CONFIRMADO
    for tipo in (
        TipoEvidencia.RESPONSIVIDADE_CELULAR,
        TipoEvidencia.BOTAO_WHATSAPP,
        TipoEvidencia.FORMULARIO_CONTATO,
    ):
        assert evidencias[tipo].indica_problema
        assert evidencias[tipo].nivel_certeza is NivelCerteza.SINAL_FORTE
    cta = evidencias[TipoEvidencia.CHAMADA_PARA_ACAO]
    assert cta.indica_problema and cta.nivel_certeza is NivelCerteza.INFERENCIA


def test_redirecionamento_para_https_conta_como_seguro():
    resultado = ResultadoSite("https://a.com/", HTML_COMPLETO)
    evidencias = _por_tipo(analisar_site("http://a.com", SiteFalso(resultado)))
    assert not evidencias[TipoEvidencia.HTTPS].indica_problema


def test_sem_url_e_desconhecido():
    (evidencia,) = analisar_site(None, SiteFalso(None))
    assert evidencia.nivel_certeza is NivelCerteza.DESCONHECIDO
    assert evidencia.tipo is TipoEvidencia.DISPONIBILIDADE_SITE


def test_falha_de_acesso_e_desconhecido_e_nao_acusa_problemas_do_site():
    (evidencia,) = analisar_site(
        "https://a.com", SiteFalso(ResultadoSite(None, None, "tempo esgotado"))
    )
    assert evidencia.nivel_certeza is NivelCerteza.DESCONHECIDO
    assert "tempo esgotado" in evidencia.valor
