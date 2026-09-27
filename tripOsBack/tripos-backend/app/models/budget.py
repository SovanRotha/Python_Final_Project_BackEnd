from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Budget(Base):
    __tablename__ = "budgets"

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

    total_budget = Column(
        Numeric(12, 2),
        nullable=False
    )

    saved_amount = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    spent_amount = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    currency = Column(
        String(10),
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

    trip = relationship(
        "Trip",
        back_populates="budget"
    )