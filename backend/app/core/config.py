"""
Application Configuration
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Country Momentum Index API"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str
    DATABASE_URL_ASYNC: str

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # External API Keys
    FRED_API_KEY: str = ""
    WORLD_BANK_API_KEY: str = ""

    # Scheduler
    DATA_UPDATE_CRON: str = "0 2 1 * *"
    ENABLE_SCHEDULER: bool = False

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
