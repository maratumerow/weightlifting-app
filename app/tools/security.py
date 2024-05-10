from app.constants import password_context


def hash_string(password: str) -> str:
    """Hash a password using bcrypt."""

    return password_context.hash(password)


def is_password_valid(password: str, hashed_pass: str) -> bool:
    """Verify a password against a hashed password."""

    return password_context.verify(password, hashed_pass)
