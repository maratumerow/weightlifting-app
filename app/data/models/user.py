from sqlalchemy.orm import Mapped, mapped_column

from app.constants import UserGroup
from app.data.models.base import Base
from app.data.models.base_fields import created_at, int_pk, updated_at


class User(Base):
    """
    User model.
    """

    __tablename__ = "users"

    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str] = mapped_column(default="")
    last_name: Mapped[str] = mapped_column(default="")
    image: Mapped[str] = mapped_column(default="")
    is_active: Mapped[bool] = mapped_column(default=True)
    email_subscribe: Mapped[bool] = mapped_column(default=True)
    group: Mapped[UserGroup] = mapped_column(default=UserGroup.USER)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
