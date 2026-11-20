from app.models import NivelCerteza, TipoEvidencia
from app.services.scoring import avaliar
from app.services.site_analysis.analyzer import EvidenciaColetada


def _ev(tipo, problema, nivel, valor="x"):
    return EvidenciaColetada(tipo, valor, nivel, "teste", problema)


def test_sem_problemas_pontua_zero():
    resultado = avaliar([_ev(TipoEvidencia.HTTPS, False, NivelCerteza.CONFIRMADO)])
    assert resultado.pontuacao == 0 and resultado.problemas == []


def test_certeza_menor_pesa_menos():
    confirmado = avaliar([_ev(TipoEvidencia.BOTAO_WHATSAPP, True, NivelCerteza.CONFIRMADO)])
    inferido = avaliar([_ev(TipoEvidencia.BOTAO_WHATSAPP, True, NivelCerteza.INFERENCIA)])
    assert confirmado.pontuacao == 20
    assert inferido.pontuacao == 12
    assert confirmado.pontuacao > inferido.pontuacao


def test_problemas_ordenados_e_nivel_principal():
    resultado = avaliar(
        [
            _ev(TipoEvidencia.CHAMADA_PARA_ACAO, True, NivelCerteza.INFERENCIA),
            _ev(TipoEvidencia.RESPONSIVIDADE_CELULAR, True, NivelCerteza.SINAL_FORTE),
            _ev(TipoEvidencia.HTTPS, True, NivelCerteza.CONFIRMADO),
        ]
    )
    assert resultado.problemas == [
        "Sem versão para celular",
        "Site não seguro (sem HTTPS)",
        "Sem chamada para ação clara",
    ]
    assert resultado.nivel_certeza is NivelCerteza.SINAL_FORTE
    assert resultado.pontuacao == int(35 * 0.85 + 25 + 10 * 0.6 + 0.5)


def test_pontuacao_limitada_a_100():
    todos = [_ev(tipo, True, NivelCerteza.CONFIRMADO) for tipo in TipoEvidencia]
    assert avaliar(todos).pontuacao == 100


def test_site_inexistente_x_inacessivel():
    inexistente = avaliar(
        [
            _ev(
                TipoEvidencia.DISPONIBILIDADE_SITE,
                True,
                NivelCerteza.DESCONHECIDO,
                "Site não encontrado",
            )
        ]
    )
    inacessivel = avaliar(
        [
            _ev(
                TipoEvidencia.DISPONIBILIDADE_SITE,
                True,
                NivelCerteza.DESCONHECIDO,
                "Site inacessível (tempo esgotado)",
            )
        ]
    )
    assert inexistente.problemas == ["Sem site encontrado"] and inexistente.pontuacao == 64
    assert inacessivel.problemas == ["Site inacessível"] and inacessivel.pontuacao == 32
