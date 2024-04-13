from pydantic import EmailStr, constr

from app.schemas.user import UserCreate


class UserCreateApi(UserCreate):
    """Схема создания пользователя"""

    email: EmailStr
    password: constr(
        min_length=8,
        max_length=20
    )