from sqlalchemy import select

from app.data.models.user import User
from app.data.repositories.interfaces import IUserRepository
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate, UserExists, UserUpdate
from app.tools.security import hash_password


class UserRepository(IUserRepository):
    """User repository."""

    def get_user_by_id(self, user_id: int) -> User | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        return user

    def get_user_by_email(self, email: str) -> UserSchema | None:
        user = self.db.query(User).filter(User.email == email).first()
        return user

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

    def get_users(self, skip: int = 0, limit: int = 100) -> list[UserSchema]:
        users = self.db.query(User).offset(skip).limit(limit).all()
        return [
            UserSchema.model_validate(user, from_attributes=True)
            for user in users
        ]

    def create_user(self, user: UserCreate) -> UserSchema:
        db_user = User(
            email=user.email,
            username=user.username,
            password=hash_password(user.password),
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return UserSchema.model_validate(db_user, from_attributes=True)

    def update_user(
        self, db_user: User, user_update_data: UserUpdate
    ) -> UserSchema:
        for field, value in user_update_data.model_dump().items():
            if value is not None:
                setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        return UserSchema.model_validate(db_user, from_attributes=True)

    def delete_user(self, user: UserSchema) -> None:
        self.db.delete(user)
        self.db.commit()
