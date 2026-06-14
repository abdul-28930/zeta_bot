from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    discord_token: str
    openai_api_key: str = ""
    database_url: str = "postgresql+asyncpg://zeta:zeta@localhost:5432/zeta_db"
    redis_url: str = "redis://localhost:6379/0"
    nano_model: str = "gpt-5.4-nano"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
