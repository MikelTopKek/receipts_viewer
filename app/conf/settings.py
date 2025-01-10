from pathlib import Path
from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class Env(str, Enum):
    """List of possible environments"""

    LOCAL = "LOCAL"
    TEST = "TEST"


class Settings(BaseSettings):
    """Base settings for all environments"""

    ENV: Env = Env.TEST
    DEBUG: bool = False
    PORT: int = 8080

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres_db"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_HOST_SLAVE: str = "localhost"
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_DRIVER_SYNC: str = "postgresql+psycopg2"


    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    @property
    def sqlalchemy_database_uri(self) -> str:
        """Database URI for the database connect"""
        if self.ENV == Env.TEST:
            return f"{self.DB_DRIVER}://{self.POSTGRES_TEST_USER}:{self.POSTGRES_TEST_PASSWORD}@{self.POSTGRES_TEST_HOST}:{self.POSTGRES_TEST_PORT}/{self.POSTGRES_TEST_DB}"

        return f"{self.DB_DRIVER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()