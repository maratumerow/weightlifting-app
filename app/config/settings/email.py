from pydantic_settings import BaseSettings


class MailSettings(BaseSettings):
    host: str = "smtp.mailosaur.net"
    username: str = "3ct2arwt@mailosaur.net"
    password: str = "ggSibYTZeO5OkH0GNyWiupdKSJcY6cSU"
    port: int = 587
