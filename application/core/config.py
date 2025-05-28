from pathlib import Path
from typing import ClassVar
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


# load environment variables from .env file
load_dotenv()


# application settings class, 
# that loads configuration from environment variables
class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str


    #pydantic configuration
    class Config:
        env_file: ClassVar[str] = ".env"
        env_file_encoding: ClassVar[str] = "utf-8"
        case_sensitive: ClassVar[bool] = True


# project base directory
BASE_DIR: Path = Path(__file__).parent.parent


# application settings instance
SETTINGS = Settings()