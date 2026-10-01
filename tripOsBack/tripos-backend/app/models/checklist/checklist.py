from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Checklist(Base):
    __tablename__ = "checklists"

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

    title = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    trip = relationship(
        "Trip",
        back_populates="checklists"
    )

    items = relationship(
        "ChecklistItem",
        back_populates="checklist"
    )
