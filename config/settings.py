from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Skill Demand Predictor"
    environment: str = "development"
    database_url: str = "sqlite:///./skill_demand_predictor.db"
    database_user: str | None = None
    database_password: str | None = None
    database_host: str | None = None
    database_port: str | None = None
    database_name: str | None = None
    default_forecast_horizon: int = 3
    model_registry_path: str = "data/processed/model_registry.json"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
