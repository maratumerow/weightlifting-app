from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


from app.api.dependencies.db import user_repo_dep
from app.data.repositories.user import UserRepository
from app.schemas.user import User
from app.services.auth.tools import check_token_exp, decode_token
from app.services.users import get_user_by_email_service

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login/", scheme_name="JWT")


def get_current_active_user_dep(
    token: str = Depends(reuseable_oauth),
    user_repo: UserRepository = Depends(user_repo_dep),
) -> User:
    """Get the current and active user."""

    token_data = decode_token(token)
    check_token_exp(token_data)
    user_email = token_data.sub
    return get_user_by_email_service(
        user_repo=user_repo,
        user_email=user_email,
    )
