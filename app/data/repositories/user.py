from sqlalchemy import select

from app.data.models.user import User
from app.data.repositories.interfaces import IUserRepository
from app.schemas.user import UserCreate, UserExists, UserUpdate
from app.tools.security import hash_password


class UserRepository(IUserRepository):
    """User repository."""

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_username_and_email_exists(
        self, username: str, email: str
    ) -> UserExists:
        subq_username = (
            select(User.username).where(User.username == username)
        ).exists()
        subq_email = (select(User.email).where(User.email == email)).exists()

        result = self.db.execute(
            select(
                subq_username.label("u_name"), subq_email.label("u_email")
            ).limit(1),
        ).first()

        is_username = result.u_name if result else False
        is_email = result.u_email if result else False

        return UserExists(
            is_username=is_username,
            is_email=is_email,
        )

    def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate) -> User:
        db_user = User(
            email=user.email,
            username=user.username,
            password=hash_password(user.password),
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, db_user: User, user_update_data: UserUpdate) -> User:
        for field, value in user_update_data.model_dump().items():
            if value is not None:
                setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
