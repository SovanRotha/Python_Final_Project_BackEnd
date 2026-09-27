from sqlalchemy.orm import Session

from app.models.trip.trip import Trip


def list_user_trips(db: Session, user_id: int) -> list[Trip]:
    return db.query(Trip).filter(Trip.user_id == user_id).all()
