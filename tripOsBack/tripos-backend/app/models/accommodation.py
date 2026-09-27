from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Accommodation(Base):
    __tablename__ = "accommodations"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    trip_id = Column(
        BigInteger,
        ForeignKey("trips.id"),
        nullable=False,
        index=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    address = Column(
        Text,
        nullable=True
    )

    check_in = Column(
        DateTime,
        nullable=False
    )

    check_out = Column(
        DateTime,
        nullable=False
    )

    room_type = Column(
        String(100),
        nullable=True
    )

    confirmation_number = Column(
        String(255),
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
        back_populates="accommodations"
    )