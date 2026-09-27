from datetime import datetime, time, timezone
from enum import Enum

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    Time,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class PlaceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Place(Base):
    __tablename__ = "places"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    destination_id = Column(
        BigInteger,
        ForeignKey("destinations.id"),
        nullable=False,
        index=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    category = Column(
        String(100),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    address = Column(
        Text,
        nullable=True
    )

    latitude = Column(
        Numeric(10, 7),
        nullable=True
    )

    longitude = Column(
        Numeric(10, 7),
        nullable=True
    )

    estimated_cost = Column(
        Numeric(10, 2),
        nullable=True
    )

    opening_time = Column(
        Time,
        nullable=True
    )

    closing_time = Column(
        Time,
        nullable=True
    )

    best_time_to_visit = Column(
        String(100),
        nullable=True
    )

    website = Column(
        String(500),
        nullable=True
    )

    rating = Column(
        Numeric(3, 2),
        nullable=True
    )

    status = Column(
        SQLEnum(PlaceStatus, name="place_status"),
        default=PlaceStatus.ACTIVE,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    destination = relationship(
        "Destination",
        back_populates="places"
    )

    itinerary_items = relationship("ItineraryItem", back_populates="place")
    photos = relationship("PlacePhoto", back_populates="place")
    tips = relationship("PlaceTip", back_populates="place")
    saved_by_users = relationship("SavedPlace", back_populates="place")
