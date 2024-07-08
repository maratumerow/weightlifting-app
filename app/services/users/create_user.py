from app.exceptions.exc_400 import ObjectsAlreadyCreated
from app.schemas.user import UserCreate, User as UserSchema
from app.services.gateways.email import push_user_email_service
from app.services.interfaces.users import IUserCreateService


class UserCreateService(IUserCreateService):
    """Service for creating a user."""

    def __call__(self, user: UserCreate) -> UserSchema | None:

        check_user = self.user_repo.get_username_and_email_exists(
            username=user.username,
            email=user.email,
        )
        error_msgs: list[str] = []
        if check_user.is_email:
            error_msgs.append("User with this email already registered")
        if check_user.is_username:
            error_msgs.append("User with this username already registered")

        if error_msgs:
            raise ObjectsAlreadyCreated(detail=error_msgs)

        user_in = self.user_repo.create_user(user=user)
        push_user_email_service(email=user.email)
        return user_in
