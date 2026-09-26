from app.models.user import User


class UserController:
    def __init__(self, user: User):
        self.user = user

    def get_current_user(self) -> User:
        return self.user