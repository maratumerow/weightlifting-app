from pydantic import BaseModel, EmailStr


class TokenInfo(BaseModel):
    """Model for token information."""

    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    """Model for token payload."""

    sub: EmailStr
    exp: int
