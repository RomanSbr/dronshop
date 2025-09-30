from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets


class Settings(BaseSettings):
    # Use environment variables directly in Docker
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Dronshop API"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14
    JWT_ALGORITHM: str = "HS256"

    DATABASE_URL: str | None = None

    SMS_CODE_LENGTH: int = 6
    SMS_CODE_TTL_SECONDS: int = 300

    # Where product folders with images live
    UPLOADS_DIR: str = "/app/uploads_temp"

    # Dev settings
    DEV_LOGIN_ENABLED: bool = False
    DEV_SEED: bool = False

    # CORS
    # Comma-separated list of origins, e.g. "http://localhost:5173,https://example.com"
    ALLOWED_ORIGINS: str = "http://localhost:5173"


settings = Settings()
