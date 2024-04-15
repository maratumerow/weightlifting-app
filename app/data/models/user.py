from sqlalchemy.orm import Mapped, mapped_column

from app.constants import UserGroupType
from app.data.models.base import Base
from app.data.models.base_fields import int_pk, created_at


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
    image: Mapped[str] = mapped_column(unique=True, default="")
    is_active: Mapped[bool] = mapped_column(default=False)
    email_subscribe: Mapped[bool] = mapped_column(default=True)
    group: Mapped[UserGroupType] = mapped_column(default=UserGroupType.USER)
    exercises: Mapped[int] = mapped_column(default=0)
    workout_program: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[created_at]
