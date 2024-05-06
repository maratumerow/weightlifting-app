from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError

from app.api.dependencies import user_repo_dep
from app.constants import auth_jwt
from app.data.repositories.user import UserRepository
from app.schemas.user import TokenPayload, User

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login/", scheme_name="JWT")


def get_current_and_active_user(
    token: str = Depends(reuseable_oauth),
    user_repo: UserRepository = Depends(user_repo_dep),
) -> User:
    try:
        payload = jwt.decode(
            token, auth_jwt.JWT_SECRET_KEY, algorithms=[auth_jwt.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_email = str(payload.get("sub"))

    user = user_repo.get_user_by_email(user_email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user
