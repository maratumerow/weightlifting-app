from sqlalchemy.orm import Session

from app.data.models.user import User
from app.data.security import get_password_hash
from app.schemas.user import UserCreate



class UserRepository:

    def __init__(self, db: Session):
        self.db = db


    def get_user(self, user_id: int) -> User | None:
        """Get a user by ID."""

        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email."""

        return self.db.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get a list of users with optional skipping and limiting."""

        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate) -> User:
        """Create a user."""

        fake_hashed_password=get_password_hash(user.password)
        db_user=User(
            email=user.email,
            username=user.username,
            password=fake_hashed_password,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
