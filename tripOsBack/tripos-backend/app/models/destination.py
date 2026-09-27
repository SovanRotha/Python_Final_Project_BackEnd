from app.core.database import Base
from app.models.base import ResourceMixin
from datetime import datetime, timezone

from sqlalchemy import BigInteger, Column, DateTime, DECIMAL, Integer, String, Text



class Destination(ResourceMixin, Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key = True, index = True)

    name = Column(String(255), nullable = False)
    country =  Column(String(255), nullable = False)

    country_code = Column(String(10), nullable=False)

    description = Column(Text, nullable=True)
    image = Column(String(500), nullable=True)

    currency = Column(String(10), nullable=True)
    language = Column(String(100), nullable=True)
    timezone = Column(String(100), nullable=True)

    best_time = Column(Text, nullable=True)

    average_daily_cost = Column(
        DECIMAL(10, 2),
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