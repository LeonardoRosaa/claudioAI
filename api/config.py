from pydantic_settings import BaseSettings, SettingsConfigDict

import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env.dev", env_file_encoding="utf-8", case_sensitive=True
    )

    ENV: str
    HOST: str
    PORT: int
    OPENAI_KEY: str
    AZURE_URL: str
    VECTOR_DB_KEY: str

class LocalDevSettings(Settings):
    model_config = SettingsConfigDict(
        env_file="./.env.dev", env_file_encoding="utf-8", case_sensitive=True
    )
    ENV: str = "dev"

def get_settings(env: str = "dev"):
    if env.lower() == "dev":
        return LocalDevSettings()
    
    raise ValueError('Invalid environment')

_env = os.environ.get('ENV', 'dev')

settings = get_settings(_env)