from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    """
    Base model for user with email and username attributes.
    """

    email: str
    username: str


class UserCreate(UserBase):
    """
    Model for creating a new user with password attribute.
    """

    password: str


class User(UserBase):
    """
    Model representing a user with ID, email, username, and creation timestamp.
    """

    id: int
    created_at: datetime

    class Config:
        from_attributes = True
