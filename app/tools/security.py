import base64
import hashlib
import hmac

PWD_HASH_SALT = base64.b64decode("salt")
PWD_HASH_ITERATIONS = 100_000


def generate_password_digest(password: str) -> bytes:
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
    return base64.b64encode(generate_password_digest(password)).decode("utf-8")


def compare_password(hash_password: str | bytes, password: str) -> bool:
    """
    Compare a hashed password with a password. Return True if they match.
    """
    return hmac.compare_digest(
        base64.b64decode(hash_password), generate_password_digest(password)
    )
