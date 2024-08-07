from pydantic import BaseModel


class MailBody(BaseModel):
    """Model for email body."""

    to: list[str]
    subject: str
    body: str
