import datetime

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """Base model for user with email and username attributes."""

    email: str
    username: str


class UserCreate(UserBase):
    """Model for creating a new user with password attribute."""

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
    updated_at: datetime.datetime


class UserUpdate(UserBase):
    """Model for updating an existing attributes."""

    password: str
    first_name: str
    last_name: str
    image: str
    email_subscribe: bool


class DeleteUserResponse(BaseModel):
    """Model for response to user deletion."""

    detail: str
    status: bool


class UserExists(BaseModel):
    is_username: bool = False
    is_email: bool =False