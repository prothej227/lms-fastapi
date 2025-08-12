from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    secret_key: str = "thisisthesecretkey"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_uri: str = "sqlite+aiosqlite:///./test.db"
    database_echo: bool = False
    database_connect_args: dict = {"check_same_thread": False}
    cors_allow_origins: list = ["http://localhost:8080"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    sqlalchemy_default_batch_size: int = 500
    model_config = SettingsConfigDict(env_file=".env")
    timezone: str = "Asia/Manila"


@lru_cache()
def get_settings() -> Settings:
    """Get the settings from env"""
    return Settings()
