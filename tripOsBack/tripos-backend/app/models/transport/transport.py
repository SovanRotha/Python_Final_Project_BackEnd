from datetime import datetime
from enum import Enum

from sqlalchemy import (
    BigInteger,
    Column,
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


class TransportType(str, Enum):
    FLIGHT = "flight"
    TRAIN = "train"
    BUS = "bus"
    TAXI = "taxi"
    BOAT = "boat"
    OTHER = "other"


class Transport(Base):
    __tablename__ = "transports"

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

    type = Column(
        SQLEnum(
            TransportType,
            name="transport_type"
        ),
        nullable=False
    )

    provider = Column(
        String(255),
        nullable=True
    )

    from_location = Column(
        String(255),
        nullable=False
    )

    to_location = Column(
        String(255),
        nullable=False
    )

    departure_time = Column(
        DateTime(timezone=True),
        nullable=False
    )

    arrival_time = Column(
        DateTime(timezone=True),
        nullable=False
    )

    booking_number = Column(
        String(255),
        nullable=True
    )

    seat = Column(
        String(50),
        nullable=True
    )

    cost = Column(
        Numeric(12, 2),
        nullable=True
    )

    notes = Column(
        Text,
        nullable=True
    )

    trip = relationship(
        "Trip",
        back_populates="transports"
    )
