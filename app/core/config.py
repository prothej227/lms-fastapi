from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    secret_key: str = "thisisthesecretkey"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_uri: str = "sqlite+aiosqlite:///./test.db"
    database_echo: bool = False
    database_connect_args: dict = {"check_same_thread": False}
    cors_allow_origins: list = ["http://localhost:3000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    """Get the settings from env"""
    return Settings()
