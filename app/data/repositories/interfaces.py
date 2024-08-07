import abc

from sqlalchemy.orm import Session

from app.schemas.user import User as UserSchema
from app.schemas.user import (UserAuthenticate, UserCreate, UserExists,
                              UserUpdate)


class IUserRepository(abc.ABC):
    """Interface for user repository."""

    def __init__(self, db: Session):
        self.db = db

    @abc.abstractmethod
    def get_user_by_id(self, user_id: int) -> UserSchema | None:
        """Get a user by ID."""

    @abc.abstractmethod
    def get_user_by_email(self, email: str) -> UserSchema | None:
        """Get a user by email."""

    @abc.abstractmethod
    def get_user_by_username(self, username: str) -> UserAuthenticate | None:
        """Get a user by username."""

    @abc.abstractmethod
    def get_username_and_email_exists(self, username: str, email: str) -> UserExists:
        """Check if a user with the given username and email exists."""

    @abc.abstractmethod
    def get_users(self, skip: int = 0, limit: int = 100) -> list[UserSchema]:
        """Get a list of users with optional skipping and limiting."""

    @abc.abstractmethod
    def create_user(self, user: UserCreate) -> UserSchema:
        """Create a user."""

    @abc.abstractmethod
    def update_user(
        self, user_id: int, user_update_data: UserUpdate
    ) -> UserSchema | None:
        """Update a user."""

    @abc.abstractmethod
    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
