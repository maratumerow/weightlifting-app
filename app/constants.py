from enum import Enum

from passlib.context import CryptContext
from pydantic import BaseModel


class UserGroupType(str, Enum):
    """
    Enum representing user group types such as 'user', 'admin', 'moderator'.
    """

    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class AuthJWT(BaseModel):
    """JWT configuration."""

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = "JWT_SECRET_KEY"
    JWT_REFRESH_SECRET_KEY: str = "JWT_REFRESH_SECRET_KEY"


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_jwt = AuthJWT()
