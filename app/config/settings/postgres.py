from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    host: str = "db"
    port: str = "5432"
    user: str = "noname"
    password: str = "noname"
    db: str = "postgres"
    url: str = f"postgresql://{user}:{password}@{host}:{port}/{db}"
