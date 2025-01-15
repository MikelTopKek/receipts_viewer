from enum import Enum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Env(str, Enum):
    """List of possible environments"""

    LOCAL = "LOCAL"
    TEST = "TEST"


class Settings(BaseSettings):
    """Base settings for all environments"""

    SECRET_KEY: str = "some-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_ENCODE_ALGORITHM: str = "HS256"

    ENV: Env = Env.TEST
    DEBUG: bool = False
    PORT: int = 8080

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432

    DB_DRIVER: str = "postgresql+asyncpg"
    DB_DRIVER_SYNC: str = "postgresql+psycopg2"


    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    @property
    def sqlalchemy_database_uri(self) -> str:
        """Database URI for the database connect"""
        return f"{self.DB_DRIVER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
