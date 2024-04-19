from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.schemas.user import UserCreateApi, UserUpdateApi
from app.data.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User | None:
        """Get a user by ID."""

        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email."""

        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User | None:
        """Get a user by username."""

        return self.db.query(User).filter(User.username == username).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get a list of users with optional skipping and limiting."""

        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreateApi) -> User:
        """Create a user."""

        db_user = User(
            email=user.email,
            username=user.username,
            password=user.password,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(
        self, user_id: int, user_update_data: UserUpdateApi
    ) -> User:
        """Update a user."""

        db_user = self.get_user_by_id(user_id=user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db_user.email = user_update_data.email
        db_user.username = user_update_data.username
        db_user.first_name = user_update_data.first_name
        db_user.last_name = user_update_data.last_name
        db_user.image = user_update_data.image
        db_user.password = user_update_data.password
        db_user.email_subscribe = user_update_data.email_subscribe

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user: User) -> bool:
        """Delete a user."""

        self.db.delete(user)
        self.db.commit()
        return True
