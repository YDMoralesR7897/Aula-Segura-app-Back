from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Aula Segura API"
    app_env: str = "development"
    app_debug: bool = False
    app_version: str = "1.0.0"

    database_url: str = Field(
        default="sqlite:///./aula_segura.db",
        description="Database connection URL.",
    )

    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )

    jwt_secret_key: str = "change-this-secret"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    admin_profile_ids: list[int] = Field(default_factory=lambda: [1])

    password_reset_expire_minutes: int = 15
    frontend_reset_url: str = "http://localhost:5173/reset-password"

    mail_username: str | None = None
    mail_password: str | None = None
    mail_from: str | None = None
    mail_port: int = 587
    mail_server: str | None = None
    mail_from_name: str = "Aula Segura"
    mail_starttls: bool = True
    mail_ssl_tls: bool = False

    bootstrap_schema: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
