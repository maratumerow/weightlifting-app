from fastapi.exceptions import HTTPException


class ObjectsAlreadyCreated(HTTPException):
    status_code = 400
    detail = "Object already created"

    def __init__(self, detail: str = "", **kwargs):

        detail = detail or self.detail
        super().__init__(
            status_code=self.status_code,
            detail=detail,
            **kwargs,
        )
