from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.models.user import User
from app.schemas.user import UserCreate, UserExists, UserUpdate


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user(self, username: str, password: str) -> User | None:
        """Get a user by username and password."""

        return self.db.query(User).filter(
            User.username == username, User.password == password
        ).first()

    def get_user_by_id(self, user_id: int) -> User | None:
        """Get a user by ID."""

        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email."""

        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User | None:
        """Get a user by username."""

        return self.db.query(User).filter(User.username == username).first()

    def get_username_and_email_exists(
        self, username: str, email: str
    ) -> UserExists:
        """Check if a user with the given username and email exists."""

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
        """Get a list of users with optional skipping and limiting."""

        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate) -> User:
        """Create a user."""

        db_user = User(
            email=user.email,
            username=user.username,
            password=user.password,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, db_user: User, user_update_data: UserUpdate) -> User:
        """Update a user."""

        if user_update_data.first_name:
            db_user.first_name = user_update_data.first_name
        if user_update_data.last_name:
            db_user.last_name = user_update_data.last_name

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user: User) -> None:
        """Delete a user."""

        self.db.delete(user)
        self.db.commit()
