from pydantic import BaseModel


class TokenInfo(BaseModel):
    """Model for token information."""

    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    """Model for token payload."""
    
    sub: str
    exp: int
