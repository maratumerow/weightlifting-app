from pydantic import EmailStr, StringConstraints
from typing_extensions import Annotated

from app.schemas.user import UserCreate, UserUpdate


class UserCreateApi(UserCreate):
    """Схема создания пользователя"""

    email: EmailStr
    username: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=20)]


class UserUpdateApi(UserUpdate):
    """Схема обновления пользователя"""

    email: EmailStr
    username: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=20)]
    first_name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    last_name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    image: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    email_subscribe: bool
