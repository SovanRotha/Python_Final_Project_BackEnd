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
    Integer,
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

    accommodations = relationship(
        "Accommodation",
        back_populates="trip"
    )

    ai_conversations = relationship("AIConversation", back_populates="trip")
    ai_extractions = relationship("AIExtraction", back_populates="trip")
    budget = relationship("Budget", back_populates="trip", uselist=False)
    checklists = relationship("Checklist", back_populates="trip")
    documents = relationship("Document", back_populates="trip")
    expenses = relationship("Expense", back_populates="trip")
    itinerary_days = relationship("ItineraryDay", back_populates="trip")
    memories = relationship("Memory", back_populates="trip")
    notifications = relationship("Notification", back_populates="trip")
    packing_lists = relationship("PackingList", back_populates="trip")
    reminders = relationship("Reminder", back_populates="trip")
    screenshots = relationship("Screenshot", back_populates="trip")
    transports = relationship("Transport", back_populates="trip")
    members = relationship("TripMember", back_populates="trip")
    wallet = relationship("TripWallet", back_populates="trip", uselist=False)
