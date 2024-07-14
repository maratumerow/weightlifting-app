from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.data.models.base import Base

SQLALCHEMY_DATABASE_URL = (
    "postgresql://noname:noname@db:5432/postgres_weightlifting-app"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db_connect_init():
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
