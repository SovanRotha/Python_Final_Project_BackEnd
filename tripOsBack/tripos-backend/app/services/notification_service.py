from sqlalchemy.orm import Session

from app.models.notification.notification import Notification


def list_user_notifications(db: Session, user_id: int) -> list[Notification]:
    return db.query(Notification).filter(Notification.user_id == user_id).all()
