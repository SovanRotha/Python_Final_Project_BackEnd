from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Memory(Base):
    __tablename__ = "memories"

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

    description = Column(
        Text,
        nullable=True
    )

    memory_date = Column(
        Date,
        nullable=False
    )

    location = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    trip = relationship(
        "Trip",
        back_populates="memories"
    )

    user = relationship(
        "User",
        back_populates="memories"
    )

    photos = relationship(
        "MemoryPhoto",
        back_populates="memory"
    )
