from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            # if run the app locally but postgres in a docker network (I use it for debugging)
            Path(__file__).parent.parent.parent / "envs" / ".env.local"
        )
    )

    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def db_dsn(self) -> str:
        dsn = (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        return dsn
