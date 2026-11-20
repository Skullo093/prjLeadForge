from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import auth, buscas, oportunidades, perfil

configuracao = get_settings()

app = FastAPI(title="LeadForge API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=configuracao.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
for roteador in (auth.router, perfil.router, buscas.router, oportunidades.router):
    app.include_router(roteador)


@app.get("/saude", tags=["infra"])
def saude() -> dict:
    return {"status": "ok", "modo": configuracao.modo_efetivo}
