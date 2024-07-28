from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.data.models.base import Base

engine = create_engine(settings.postgres.url)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db_connect_init():
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
