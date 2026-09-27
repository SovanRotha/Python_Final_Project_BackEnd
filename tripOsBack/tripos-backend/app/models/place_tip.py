from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class PlaceTipType(str, Enum):
    BEST_TIME = "best_time"
    SAFETY = "safety"
    CLOTHING = "clothing"
    TRANSPORT = "transport"
    MONEY = "money"
    FOOD = "food"
    GENERAL = "general"


class PlaceTip(Base):
    __tablename__ = "place_tips"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    place_id = Column(
        BigInteger,
        ForeignKey("places.id"),
        nullable=False,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    type = Column(
        SQLEnum(PlaceTipType, name="place_tip_type"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    place = relationship(
        "Place",
        back_populates="tips"
    )