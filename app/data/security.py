def get_password_hash(password: str) -> str:
    fake_hashed_password = password + "notreallyhashed"
    return fake_hashed_password
