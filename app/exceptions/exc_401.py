from fastapi import HTTPException


class InvalidTokenException(HTTPException):
    status_code = 403
    detail = "Invalid token"

    def __init__(self, detail: str | list[str] = "", **kwargs):
        detail = detail or self.detail
        if isinstance(detail, list):
            detail = ", ".join(detail)

        super().__init__(
            status_code=self.status_code,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
            **kwargs,
        )
