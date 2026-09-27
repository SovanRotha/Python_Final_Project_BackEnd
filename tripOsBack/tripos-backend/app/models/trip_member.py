from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class TripMemberRole(str, Enum):
    OWNER = "owner"
    MEMBER = "member"


class TripMember(Base):
    __tablename__ = "trip_members"

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

    user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    role = Column(
        SQLEnum(TripMemberRole, name="trip_member_role"),
        nullable=False,
        default=TripMemberRole.MEMBER
    )

    joined_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    trip = relationship(
        "Trip",
        back_populates="members"
    )

    user = relationship(
        "User",
        back_populates="trip_memberships"
    )