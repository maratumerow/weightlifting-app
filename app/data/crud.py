from sqlalchemy.orm import Session

from data.models.user import User
from data.security import get_password_hash
from schemas.user import UserCreate


def get_user(db: Session, user_id: int) -> User | None:
    """Get a user by ID."""

    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Get a user by email."""

    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Get a list of users with optional skipping and limiting."""

    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a user."""

    fake_hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        password=fake_hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
