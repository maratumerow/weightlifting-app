import base64
import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from fastapi import Depends, HTTPException
from pydantic import BaseModel

from app.api.dependencies import user_repo_dep
from app.data.repositories.user import UserRepository

PWD_HASH_SALT = base64.b64decode("salt")
PWD_HASH_ITERATIONS = 100_000


def _generate_password_digest(password: str) -> bytes:
    """
    Generate a password digest using PBKDF2-HMAC-SHA256.
    """
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=PWD_HASH_SALT,
        iterations=PWD_HASH_ITERATIONS,
    )


def get_password_hash(password: str) -> str:
    """
    Generate a password hash and return it as a base64 encoded string.
    """
    return base64.b64encode(_generate_password_digest(password)).decode(
        "utf-8"
    )


def compare_password(hash_password: str | bytes, password: str) -> bool:
    """
    Compare a hashed password with a password. Return True if they match.
    """
    return hmac.compare_digest(
        base64.b64decode(hash_password), _generate_password_digest(password)
    )


BASE_DIR = Path(__file__).parent.parent.parent


class AuthJWT(BaseModel):
    """JWT configuration."""
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


auth_jwt = AuthJWT()


def encode_jwt(
    payload: dict[str, str],
    private_key: str = auth_jwt.private_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
    expire_minutes: int = auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    """Encode a JWT token with the given payload."""

    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta is not None:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=str(expire),
        iat=str(now),
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decoded_jwt(
    token: str | bytes,
    public_key: str = auth_jwt.public_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
):
    """Decode a JWT token with the given public key."""
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def validate_auth_user(
    username: str,
    password: str,
    user_repo: UserRepository = Depends(user_repo_dep),
):
    """Validate the user credentials."""

    user = user_repo.get_user_by_username(username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    check_password = compare_password(
        hash_password=user.password, password=password
    )
    if not check_password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    return user
