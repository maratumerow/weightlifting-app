import abc

from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserUpdate, User, UserExists


class IUserRepository(abc.ABC):
    def __init__(self, db: Session):
        self.db = db

    @abc.abstractmethod
    def get_user_by_id(self, user_id: int) -> User | None:
        ...

    @abc.abstractmethod
    def get_user_by_email(self, email: str) -> User | None:
        ...

    @abc.abstractmethod
    def get_user_by_username(self, username: str) -> User | None:
        """Get a user by username."""

    @abc.abstractmethod
    def get_username_and_email_exists(
            self, username: str, email: str
    ) -> UserExists:
        """Check if a user with the given username and email exists."""

    @abc.abstractmethod
    def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get a list of users with optional skipping and limiting."""

    @abc.abstractmethod
    def create_user(self, user: UserCreate) -> User:
        """Create a user."""

    @abc.abstractmethod
    def update_user(self, db_user: User, user_update_data: UserUpdate) -> User:
        """Update a user."""

    @abc.abstractmethod
    def delete_user(self, user: User) -> None:
        """Delete a user."""
