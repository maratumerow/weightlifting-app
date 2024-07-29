from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime, mapped_column(DateTime(timezone=True), default=func.now())
]
updated_at = Annotated[
    datetime,
    mapped_column(DateTime(timezone=True), onupdate=func.now(), default=func.now()),
]
