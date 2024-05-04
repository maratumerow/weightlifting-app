from pydantic import EmailStr, StringConstraints
from typing_extensions import Annotated

from app.schemas.user import UserCreate, UserLogin, UserUpdate


class UserCreateApi(UserCreate):
    """User create schema."""

    email: EmailStr
    username: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=20)]


class UserUpdateApi(UserUpdate):
    """User update schema."""

    first_name: (
        Annotated[str, StringConstraints(min_length=2, max_length=50)] | None
    )
    last_name: (
        Annotated[str, StringConstraints(min_length=2, max_length=50)] | None
    )


class UserLoginApi(UserLogin):
    """User login schema."""

    username: str
    email: str
