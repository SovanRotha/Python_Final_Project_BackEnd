from datetime import datetime, timezone

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class SavedPlace(Base):
    __tablename__ = "saved_places"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        index=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    place_id = Column(
        BigInteger,
        ForeignKey("places.id"),
        nullable=False,
        index=True
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="saved_places"
    )

    place = relationship(
        "Place",
        back_populates="saved_by_users"
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "place_id",
            name="uq_saved_place_user_place"
        ),
    )
