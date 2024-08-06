from pydantic_settings import BaseSettings

from app.config.settings import AppSettings, PostgresSettings


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    app: AppSettings = AppSettings()


settings = Settings()
