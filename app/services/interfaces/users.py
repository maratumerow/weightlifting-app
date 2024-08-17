import abc

from app.schemas.auth import TokenInfo
from app.schemas.user import User as UserSchema
from app.schemas.user import (UserAuthenticate, UserCreate, UserExists,
                              UserUpdate)
from app.services.interfaces.email_gateways import IEmailGateway


class IUserRepository(abc.ABC):
    """Interface for user repository."""

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
    def get_username_and_email_exists(
        self, username: str, email: str
    ) -> UserExists:
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


class IUserCreateService(abc.ABC):
    """Interface for creating a user."""

    def __init__(self, user_repo: IUserRepository, email_repo: IEmailGateway):
        self.email_repo = email_repo
        self.user_repo = user_repo

    def __call__(self, user: UserCreate) -> UserSchema | None:
        """Create a user"""


class IUsersGetService(abc.ABC):
    """Interface for getting a list of users."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(self, skip: int, limit: int) -> list[UserSchema] | None:
        """Get a list of users with optional skipping and limiting."""


class IUserUpdateService(abc.ABC):
    """Interface for updating a user."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(
        self, user_id: int, user_update_data: UserUpdate
    ) -> UserSchema | None:
        """Update a user by ID"""


class IUserGetService(abc.ABC):
    """Interface for getting a user by ID."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(self, user_id: int) -> UserSchema | None:
        """Get a user by ID"""


class IUserDeleteService(abc.ABC):
    """Interface for deleting a user."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(self, user_id: int) -> None:
        """Delete a user by ID"""


class IAuthenticationTokensService(abc.ABC):
    """Interface for creating access and refresh tokens for user."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(self, username: str, password: str) -> TokenInfo | None:
        """Create access and refresh tokens for user."""


class IUserGetByEmailService(abc.ABC):
    """Interface for getting a user by email."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(self, user_email: str) -> UserSchema | None:
        """Get a user by email."""
