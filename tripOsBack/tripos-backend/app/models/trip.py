from datetime import date, datetime, timezone
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class TripStatus(str, Enum):
    PLANNING = "planning"
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Trip(Base):
    __tablename__ = "trips"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
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

    description = Column(
        Text,
        nullable=True
    )

    start_date = Column(
        Date,
        nullable=False
    )

    end_date = Column(
        Date,
        nullable=False
    )

    currency = Column(
        String(10),
        nullable=False
    )

    budget_amount = Column(
        Numeric(12, 2),
        nullable=True
    )

    status = Column(
        SQLEnum(TripStatus, name="trip_status"),
        default=TripStatus.PLANNING,
        nullable=False
    )

    cover_image = Column(
        String(500),
        nullable=True
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

    user = relationship(
        "User",
        back_populates="trips"
    )

    destination = relationship(
        "Destination",
        back_populates="trips"
    )