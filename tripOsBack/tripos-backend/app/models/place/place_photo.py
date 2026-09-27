from app.core.database import Base
from app.models.common.base import ResourceMixin
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

from sqlalchemy import BigInteger, Column, DateTime, DECIMAL, String, Text, ForeignKey

class PlacePhoto(Base):
    __tablename__ = "place_photos"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    place_id = Column(
        BigInteger,
        ForeignKey("places.id"),
        nullable=False,
        index=True
    )

    image_path = Column(
        String(500),
        nullable=False
    )

    caption = Column(
        String(255),
         nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    place = relationship(
        "Place",
        back_populates="photos"
    )
