from fastapi.exceptions import HTTPException


class ObjectsForbiddenException(HTTPException):
    """Exception for when an object is forbidden."""

    status_code = 403
    detail = "Forbidden"

    def __init__(self, detail: str | list[str] = "", **kwargs):
        detail = detail or self.detail
        if isinstance(detail, list):
            detail = ", ".join(detail)

        super().__init__(
            status_code=self.status_code,
            detail=detail,
            **kwargs,
        )
