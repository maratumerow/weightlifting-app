from fastapi.exceptions import HTTPException


class ObjectsAlreadyCreated(HTTPException):
    status_code = 400
    detail = "Object already created"

    def __init__(self, detail: str | list[str] = "", **kwargs):
        detail = detail or self.detail
        if isinstance(detail, list):
            detail = ", ".join(detail)

        super().__init__(
            status_code=self.status_code,
            detail=detail,
            **kwargs,
        )
