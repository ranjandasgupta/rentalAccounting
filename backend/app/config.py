from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:8000"
    STATIC_DIR: str = "../frontend"
    BACKUP_DIR: str = "/mnt/nas/rental_accounting_backups"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    @field_validator("ALLOWED_ORIGINS")
    @classmethod
    def split_origins(cls, v: str):
        return [x.strip() for x in v.split(",") if x.strip()]

settings = Settings()  # loads from environment variables (.env)
