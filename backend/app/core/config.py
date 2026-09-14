from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Niriksh Intelligence API"
    database_url: str = "sqlite:///./niriksh.db"
    cors_origins: str = "http://localhost:5173"
    simulator_interval_seconds: float = 3.0
    model_config = SettingsConfigDict(env_file=".env", env_prefix="NIRIKSH_")

    @property
    def cors_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()
