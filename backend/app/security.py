import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

import jwt

from app.config import get_settings

_N, _R, _P = 2**14, 8, 1
_ALGORITMO = "HS256"


def gerar_hash_senha(senha: str) -> str:
    sal = secrets.token_bytes(16)
    derivada = hashlib.scrypt(senha.encode(), salt=sal, n=_N, r=_R, p=_P)
    return f"scrypt${_N}${_R}${_P}${sal.hex()}${derivada.hex()}"


def verificar_senha(senha: str, armazenado: str) -> bool:
    try:
        _, n, r, p, sal, esperado = armazenado.split("$")
        derivada = hashlib.scrypt(
            senha.encode(), salt=bytes.fromhex(sal), n=int(n), r=int(r), p=int(p)
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(derivada, bytes.fromhex(esperado))


def criar_token(usuario_id: int) -> str:
    configuracao = get_settings()
    expira = datetime.now(UTC) + timedelta(minutes=configuracao.token_expira_minutos)
    return jwt.encode(
        {"sub": str(usuario_id), "exp": expira}, configuracao.secret_key, algorithm=_ALGORITMO
    )


def ler_token(token: str) -> int | None:
    try:
        dados = jwt.decode(token, get_settings().secret_key, algorithms=[_ALGORITMO])
        return int(dados["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        return None
