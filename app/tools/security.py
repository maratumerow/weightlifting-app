import bcrypt


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password."""

    return bcrypt.checkpw(password.encode(), hashed_password.encode())
