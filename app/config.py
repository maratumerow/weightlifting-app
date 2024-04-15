from pydantic_settings import BaseSettings



class AppConfig(BaseSettings):
    api_title:  str = "Weightlifting API"