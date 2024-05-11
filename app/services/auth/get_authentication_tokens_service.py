from fastapi.security import OAuth2PasswordRequestForm

from app.data.repositories.user import UserRepository
from app.exceptions.exc_404 import ObjectsNotFoundException
from app.schemas.auth import TokenInfo
from app.services.auth.tools import create_access_token, create_refresh_token
from app.tools.security import is_password_valid


def get_authentication_tokens_service(
    form_data: OAuth2PasswordRequestForm,
    user_repo: UserRepository,
) -> TokenInfo:
    """Create access and refresh tokens for user."""

    db_user = user_repo.get_user_by_username(username=form_data.username)
    if not db_user or not is_password_valid(
        password=form_data.password, hashed_pass=db_user.password
    ):
        raise ObjectsNotFoundException(
            detail="Incorrect username or password",
        )

    return TokenInfo(
        access_token=create_access_token(db_user.email),
        refresh_token=create_refresh_token(db_user.email),
    )
