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


class MemoryPhoto(Base):
    __tablename__ = "memory_photos"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        index=True
    )

    memory_id = Column(
        BigInteger,
        ForeignKey("memories.id"),
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

    memory = relationship(
        "Memory",
        back_populates="photos"
    )
