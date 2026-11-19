import re
import unicodedata

# palavras-chave (sem acento) -> (chave do nicho, categorias da API de lugares)
_NICHOS: list[tuple[tuple[str, ...], str, list[str]]] = [
    (
        ("estetica", "beleza", "spa", "dermato", "salao"),
        "estetica",
        ["commercial.health_and_beauty", "service.beauty.spa"],
    ),
    (("odonto", "dentista", "dental"), "odontologia", ["healthcare.dentist"]),
    (
        ("academia", "fitness", "pilates", "musculacao", "crossfit"),
        "academia",
        ["sport.fitness.fitness_centre"],
    ),
    (("restaurante", "pizzaria", "lanchonete", "bistro"), "restaurante", ["catering.restaurant"]),
]


def normalizar(texto: str | None) -> str:
    """Minúsculas, sem acentos e com espaços simples."""
    if not texto:
        return ""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", sem_acento.lower()).strip()


def chave_do_nicho(nicho: str) -> str | None:
    texto = normalizar(nicho)
    for palavras, chave, _ in _NICHOS:
        if any(palavra in texto for palavra in palavras):
            return chave
    return None


def categorias_geoapify(nicho: str) -> list[str] | None:
    chave = chave_do_nicho(nicho)
    for _, chave_nicho, categorias in _NICHOS:
        if chave_nicho == chave:
            return categorias
    return None
