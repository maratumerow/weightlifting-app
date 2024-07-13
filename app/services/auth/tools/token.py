import logging
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.constants import auth_jwt
from app.exceptions.exc_401 import InvalidTokenException
from app.schemas.auth import TokenPayload

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login/", scheme_name="JWT")


def create_access_token(
    subject: str, expire_timedelta: timedelta | None = None
) -> str:
    """Create an access token for a user."""

    return create_token(subject, auth_jwt.JWT_SECRET_KEY, expire_timedelta)


def create_refresh_token(
    subject: str, expire_timedelta: timedelta | None = None
) -> str:
    """Create a refresh token for a user."""

    return create_token(
        subject,
        auth_jwt.JWT_REFRESH_SECRET_KEY,
        expire_timedelta,
        auth_jwt.REFRESH_TOKEN_EXPIRE_MINUTES,
    )


def create_token(
    subject: str,
    secret_key: str,
    expire_timedelta: timedelta | None = None,
    default_expire_minutes: int = auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    """Create a token for a user."""

    now = datetime.now(timezone.utc)
    expire = now + (
        expire_timedelta or timedelta(minutes=default_expire_minutes)
    )

    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, secret_key, auth_jwt.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenPayload:
    """Decode the token and return the payload."""
    try:
        payload = jwt.decode(
            token, auth_jwt.JWT_SECRET_KEY, algorithms=[auth_jwt.ALGORITHM]
        )
        return TokenPayload(**payload)
    except JWTError:
        logging.error("Could not validate credentials")
        raise InvalidTokenException(detail="Could not validate credentials")


def check_token_exp(token_data: TokenPayload) -> None:
    """Check if the token has expired."""
    if datetime.fromtimestamp(token_data.exp) < datetime.now():
        logging.error("Token has expired")
        raise InvalidTokenException(detail="Token has expired")
