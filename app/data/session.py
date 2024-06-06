from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.data.models.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///app/data/sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    # echo=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db_connect_init():
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
