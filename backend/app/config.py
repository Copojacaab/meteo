"""
    config.py:

    Cosa fa:
        Centralizza la configurazione (DB, JWT secret...) in una classe validata letta da env avrs
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "postgresql+asyncpg://meteo:meteo_dev@db:5432/meteo"
    secret_key: str = "dev-secret-key-change-in-production"

settings = Settings()

