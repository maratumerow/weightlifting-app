import logging

from app.exceptions.exc_404 import ObjectsNotFoundException
from app.schemas.auth import TokenInfo
from app.services.auth.tools import create_access_token, create_refresh_token
from app.services.interfaces.users import IAuthenticationTokensService
from app.tools.security import verify_password


class GetAuthenticationTokensService(IAuthenticationTokensService):
    """Service for creating access and refresh tokens for user."""

    def __call__(
        self,
        username: str,
        password: str,
    ) -> TokenInfo:
        """Create access and refresh tokens for user."""

        db_user = self.user_repo.get_user_by_username(username=username)

        if not db_user or not verify_password(
            password=password, hashed_password=db_user.password
        ):
            logging.error(f"Incorrect USERNAME={username} or PASSWORD")
            raise ObjectsNotFoundException(
                detail="Incorrect username or password",
            )

        return TokenInfo(
            access_token=create_access_token(db_user.email),
            refresh_token=create_refresh_token(db_user.email),
        )
