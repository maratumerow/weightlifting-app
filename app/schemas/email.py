from pydantic import BaseModel


class MailBody(BaseModel):
    """Model for email body."""

    to: str
    subject: str
    body: str
