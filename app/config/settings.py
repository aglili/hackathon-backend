import os
from typing import List

from pydantic import AnyHttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Hackathon Backend"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = os.getenv(
        "BACKEND_CORS_ORIGINS",
        [
            "http://localhost:8000",
            "https://localhost:8000",
            "http://localhost",
            "https://localhost",
        ],
    )
    PROJECT_VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"

    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = os.getenv("DB_PORT", 5432)
    DB_USERNAME: str = os.getenv("DB_USERNAME", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "root")
    DB_NAME: str = os.getenv("DB_NAME", "boilerplate")
    DB_ENGINE: str = os.getenv("DB_ENGINE", "postgresql")

    DB_URI: str = os.getenv(
        "DB_URI"
    )

    PASSWORD_REGEX: str = os.getenv(
        "PASSWORD_REGEX",
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$",
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "test_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"


    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    BUCKET_NAME: str = os.getenv("BUCKET_NAME")


    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"


settings = Settings()
