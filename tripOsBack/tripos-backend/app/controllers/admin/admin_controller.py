from sqlalchemy.orm import Session

from app.models.user.user import User


class AdminController:
    def __init__(self, db: Session):
        self.db = db

    def count_users(self) -> int:
        return self.db.query(User).count()
