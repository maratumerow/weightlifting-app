from fastapi.exceptions import HTTPException


class ObjectsNotFoundException(HTTPException):
    """Exception for when an object is not found."""

    status_code = 404
    detail = "Object Not Found"

    def __init__(self, detail: str | list[str] = "", **kwargs):
        detail = detail or self.detail
        if isinstance(detail, list):
            detail = ", ".join(detail)

        super().__init__(
            status_code=self.status_code,
            detail=detail,
            **kwargs,
        )
