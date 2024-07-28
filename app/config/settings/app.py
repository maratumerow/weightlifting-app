from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    api_title: str = "Weightlifting API"
