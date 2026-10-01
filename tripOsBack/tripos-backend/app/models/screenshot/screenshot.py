from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    JSON,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class ScreenshotType(str, Enum):
    FLIGHT = "flight"
    HOTEL = "hotel"
    TICKET = "ticket"
    TRANSPORT = "transport"
    PLACE = "place"
    PRICE = "price"
    MAP = "map"
    BOOKING = "booking"
    OTHER = "other"


class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        index=True
    )

    trip_id = Column(
        BigInteger,
        ForeignKey("trips.id"),
        nullable=False,
        index=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    type = Column(
        SQLEnum(
            ScreenshotType,
            name="screenshot_type"
        ),
        nullable=False
    )

    image_path = Column(
        String(500),
        nullable=False
    )

    extracted_data = Column(
        JSON,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    trip = relationship(
        "Trip",
        back_populates="screenshots"
    )

    user = relationship(
        "User",
        back_populates="screenshots"
    )

    ai_extractions = relationship(
        "AIExtraction",
        back_populates="screenshot"
    )
