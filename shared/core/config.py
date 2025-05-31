from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    SEARCH_SERVICE_HOST: str
    SEARCH_SERVICE_PORT: int
    SEARCH_SERVICE_PATH: str

    ELASTICSEARCH_INDEX_NAME: str
    ELASTICSEARCH_SEARCH_SIZE: int
    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_PORT: int
    SCHEDULE_INTERVAL_SECONDS: int
    
    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )
    
    @property
    def elastic_search_url(self) -> str:
        return (
            f"http://{self.ELASTICSEARCH_HOST}:"
            f"{self.ELASTICSEARCH_PORT}"
        )

    @property
    def search_service_url(self) -> str:
        return (
            f"http://{self.SEARCH_SERVICE_HOST}:"
            f"{self.SEARCH_SERVICE_PORT}"
            f"{self.SEARCH_SERVICE_PATH}"
        )
    
    class Config:
        env_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "..",
            ".env"
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()