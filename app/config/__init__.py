from pydantic_settings import BaseSettings

from app.config.settings import AppSettings, MailSettings, PostgresSettings


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    app: AppSettings = AppSettings()
    email: MailSettings = MailSettings()


settings = Settings()
