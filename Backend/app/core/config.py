from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "SIMLABA Kota Tegal"
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = "er1gDEZKTvJ9UAJ0VF61M5dnsJo2hIxpgJ3npUKUlMy"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "monevrkpd"
    POSTGRES_PASSWORD: str = "heriprihanto140286"
    POSTGRES_DB: str = "dalev_kota_tegal_2027"

    BACKEND_CORS_ORIGINS: str = "http://localhost,http://localhost:5173,http://localhost:8000,http://127.0.0.1:5173"

    # SMTP Emails
    SMTP_HOST: str = "mail.tegalkota.go.id"
    SMTP_USER: str = "bapperida"
    SMTP_PASSWORD: str = "b4pp3r1d4@t3g4lk0t4"
    EMAILS_FROM_EMAIL: str = "bapperida@tegalkota.go.id"
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 465

    @property
    def cors_origins(self) -> List[str]:
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]
        return []

    @property
    def DATABASE_URL(self) -> str:
        # SQLAlchemy postgresql+psycopg connection string
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
