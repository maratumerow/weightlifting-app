from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.data.repositories.user import UserRepository
from app.schemas.user import TokenInfo
from app.tools.security import (create_access_token, create_refresh_token,
                                verify_password)


def login_service(
    form_data: OAuth2PasswordRequestForm, user_repo: UserRepository
) -> TokenInfo:
    """Create access and refresh tokens for user."""

    db_user = user_repo.get_user_by_username(username=form_data.username)
    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )

    if not verify_password(
        password=form_data.password, hashed_pass=db_user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
        )

    return TokenInfo(
        access_token=create_access_token(db_user.email),
        refresh_token=create_refresh_token(db_user.email),
    )
