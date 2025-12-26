from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import field_validator
import json


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 30
    database_uri: str
    database_echo: bool
    database_connect_args: dict
    cors_allow_origins: list = []
    cors_allow_credentials: bool
    cors_allow_methods: list
    cors_allow_headers: list
    sqlalchemy_default_batch_size: int = 500

    timezone: str
    ref_value_mappings_path: str
    model_config = SettingsConfigDict(env_file=".env")

    @field_validator(
        "cors_allow_origins", "cors_allow_methods", "cors_allow_headers", mode="before"
    )
    def parse_json_list(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v

    @field_validator("database_connect_args", mode="before")
    def parse_json_dict(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


@lru_cache()
def get_settings() -> Settings:
    """Get the settings from env"""
    return Settings()  # type: ignore
