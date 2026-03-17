# src/infrastructure/config/settings.py

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # === Core App Settings ===
    app_name: str = Field(default="Real Estate Ridge Agent")
    app_env: str = Field(default="development")
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)

    # === Logging ===
    log_level: str = Field(default="INFO")
    log_requests: bool = Field(default=True)

    # === Domain Parameters ===
    max_file_size_mb: int = Field(default=10)
    default_gamma: float = Field(default=1.0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # APP_NAME -> app_name
        extra="ignore",  # Игнорировать лишние поля
    )


@lru_cache
def get_settings() -> Settings:
    """
    Кэшируем настройки.
    Создаётся один экземпляр на всё приложение.
    """
    return Settings()


settings = get_settings()
