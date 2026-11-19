"""Fonte de empresas simulada, para demonstrar o sistema sem chaves de API nem internet.

Cada empresa recebe um "padrão" que define como o site dela será simulado. O padrão vai na
própria URL (`?p=N`), então `DemoSiteFetcher` monta o HTML sem guardar estado.
"""

import re
from urllib.parse import quote

from app.services.discovery.base import EmpresaDescoberta, ProviderError
from app.services.niches import chave_do_nicho, normalizar

# (https, viewport, whatsapp, formulario, cta) | None = sem site | "inacessivel"
PADROES: list[tuple[bool, bool, bool, bool, bool] | str | None] = [
    (False, False, False, False, False),
    (False, False, False, True, True),
    None,
    (True, True, False, True, False),
    (False, True, True, False, True),
    "inacessivel",
    (True, True, True, True, True),
    (True, False, True, True, True),
]

_NOMES = {
    "estetica": [
        "Clínica Bela Forma",
        "Studio Corpo & Alma",
        "Espaço Vita Estética",
        "Dermacare Estética Avançada",
        "Clínica Renove",
        "Estética Pura Pele",
        "Espaço Bem Viver",
        "Clínica Harmonia Estética",
    ],
    "odontologia": [
        "Odonto Sorriso",
        "Dentalis",
        "Clínica Sorriso Pleno",
        "Dr. Marcos Lima Odontologia",
        "OdontoVida",
        "Implante Center",
    ],
    "academia": [
        "Academia Ritmo Vital",
        "Fit Center",
        "Studio Pilates Equilíbrio",
        "Corpo em Movimento",
        "Power Gym",
        "Academia Movimento Livre",
    ],
    "restaurante": [
        "Cantina Bella Massa",
        "Restaurante Sabor da Terra",
        "Pizzaria Forno de Ouro",
        "Bistrô Quintal",
        "Churrascaria Fogo Brasa",
        "Cozinha da Vó Lia",
    ],
}
_BAIRROS = [
    "Campolim",
    "Jardim dos Estados",
    "Centro",
    "Trujillo",
    "Vila Hortência",
    "Jardim Europa",
    "Éden",
    "Vila Barcelona",
]


def _slug(texto: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", normalizar(texto))


class DemoPlacesProvider:
    def buscar(self, nicho: str, cidade: str, estado: str, limite: int) -> list[EmpresaDescoberta]:
        if normalizar(cidade) == "erro":
            raise ProviderError("PLACES_503", "O serviço de busca está indisponível no momento.")
        chave = chave_do_nicho(nicho) or "generico"
        nomes = _NOMES.get(chave) or [f"{nicho.strip().title()} Exemplo {i}" for i in range(1, 9)]
        empresas = []
        for indice, nome in enumerate(nomes[:limite]):
            padrao = PADROES[indice % len(PADROES)]
            url = None
            if padrao is not None:
                https = padrao[0] if isinstance(padrao, tuple) else True
                esquema = "https" if https else "http"
                url = f"{esquema}://www.{_slug(nome)}.com.br/?p={indice % len(PADROES)}"
            empresas.append(
                EmpresaDescoberta(
                    external_id=f"demo:{chave}:{_slug(cidade)}:{indice}",
                    nome=nome,
                    nicho=nicho.strip(),
                    cidade=cidade.strip(),
                    estado=estado,
                    bairro=_BAIRROS[indice % len(_BAIRROS)],
                    endereco=f"Rua {quote(_slug(nome)[:8].title())}, {100 + indice * 37}",
                    telefone=f"(15) 3{200 + indice * 11}-{4000 + indice * 73}",
                    url_site=url,
                )
            )
        return empresas
