from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="postgres_")
    host: str = "localhost"
    port: str = "5432"
    user: str = "postgres"
    password: str = "postgres"
    db: str = "postgres-db"

    @property
    def url(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.db}"
        )
