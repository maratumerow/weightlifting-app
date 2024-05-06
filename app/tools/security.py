from datetime import datetime, timedelta, timezone

from jose import jwt

from app.constants import auth_jwt, password_context


def get_hashed_password(password: str) -> str:
    """Hash a password using bcrypt."""

    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    """Verify a password against a hashed password."""

    return password_context.verify(password, hashed_pass)


def create_access_token(
    subject: str,
    expire_timedelta: timedelta | None = None,
) -> str:
    """Create an access token for a user."""

    now = datetime.now(timezone.utc)
    if expire_timedelta is not None:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(
        to_encode, auth_jwt.JWT_SECRET_KEY, auth_jwt.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: str, expire_timedelta: timedelta | None = None
) -> str:
    """Create a refresh token for a user."""
    
    now = datetime.now(timezone.utc)
    if expire_timedelta is not None:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=auth_jwt.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(
        to_encode, auth_jwt.JWT_REFRESH_SECRET_KEY, auth_jwt.ALGORITHM
    )
    return encoded_jwt
