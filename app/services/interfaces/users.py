import abc

from fastapi.security import OAuth2PasswordRequestForm

from app.data.models.user import User
from app.data.repositories.interfaces import IUserRepository
from app.schemas.auth import TokenInfo
from app.schemas.user import UserCreate, UserUpdate


class IUserCreateService(abc.ABC):
    """Interface for creating a user."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(self, user: UserCreate) -> User | None:
        """Create a user"""


class IUsersGetService(abc.ABC):
    """Interface for getting a list of users."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(self, skip: int, limit: int) -> list[User] | None:
        """Get a list of users with optional skipping and limiting."""


class IUserUpdateService(abc.ABC):
    """Interface for updating a user."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(
        self, user_id: int, user_update_data: UserUpdate
    ) -> User | None:
        """Update a user by ID"""


class IUserGetService(abc.ABC):
    """Interface for getting a user by ID."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(self, user_id: int) -> User | None:
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

    def __call__(
        self, form_data: OAuth2PasswordRequestForm
    ) -> TokenInfo | None:
        """Create access and refresh tokens for user."""


class IUserGetByEmailService(abc.ABC):
    """Interface for getting a user by email."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(self, user_email: str) -> User | None:
        """Get a user by email."""
