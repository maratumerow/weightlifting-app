import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    """Base model for user with email and username attributes."""

    email: str
    username: str


class UserCreate(UserBase):
    """Model for creating a new user with password attribute."""

    password: str


class UserAuthenticate(BaseModel):
    """Model for authenticating a user."""

    username: str
    email: str
    password: str


class User(UserBase):
    """
    Model representing a user.
    """

    id: int
    created_at: datetime.datetime
    first_name: str
    last_name: str
    image: str
    email_subscribe: bool
    is_active: bool
    updated_at: datetime.datetime


class UserUpdate(BaseModel):
    """Model for updating an existing attributes."""

    first_name: str | None
    last_name: str | None


class UserLogin(BaseModel):
    """Model for logging in a user."""

    username: str
    email: str
    password: str


class UserExists(BaseModel):
    """Model for checking if a user exists."""

    is_username: bool = False
    is_email: bool = False
