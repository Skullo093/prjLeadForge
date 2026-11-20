from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

Modo = Literal["auto", "demo", "live"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LEADFORGE_", env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./leadforge.db"
    secret_key: str = "chave-de-desenvolvimento-troque-em-producao"
    token_expira_minutos: int = 60 * 24
    mode: Modo = "auto"
    cors_origins: list[str] = ["http://localhost:5173"]

    geoapify_api_key: str = ""
    geoapify_search_endpoint: str = "https://api.geoapify.com/v1/geocode/search"
    geoapify_places_endpoint: str = "https://api.geoapify.com/v2/places"
    geoapify_timeout_segundos: float = 12.0

    site_timeout_segundos: float = 8.0
    site_max_bytes: int = 1_000_000
    site_user_agent: str = "LeadForgeBot/0.1 (analise de sites publicos)"

    @property
    def modo_efetivo(self) -> Literal["demo", "live"]:
        if self.mode == "auto":
            return "live" if self.geoapify_api_key else "demo"
        return self.mode


@lru_cache
def get_settings() -> Settings:
    return Settings()
