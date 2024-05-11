from typing import Generator

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.data.repositories.user import UserRepository
from app.data.session import SessionLocal

router = APIRouter()


def get_db() -> Generator[Session, None, None]:
    """
    Provides a database session to the dependent functions
    using FastAPI's dependency injection.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def user_repo_dep(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)
