from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.transport.transport import TransportType


class TransportCreate(BaseModel):
    trip_id: int

    type: TransportType

    provider: str | None = Field(
        default=None,
        max_length=255
    )

    from_location: str = Field(
        min_length=1,
        max_length=255
    )

    to_location: str = Field(
        min_length=1,
        max_length=255
    )

    departure_time: datetime
    arrival_time: datetime

    booking_number: str | None = Field(
        default=None,
        max_length=255
    )

    seat: str | None = Field(
        default=None,
        max_length=100
    )

    cost: Decimal | None = Field(
        default=None,
        ge=0
    )

    notes: str | None = None


class TransportUpdate(BaseModel):
    type: TransportType | None = None

    provider: str | None = Field(
        default=None,
        max_length=255
    )

    from_location: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    to_location: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    departure_time: datetime | None = None
    arrival_time: datetime | None = None

    booking_number: str | None = Field(
        default=None,
        max_length=255
    )

    seat: str | None = Field(
        default=None,
        max_length=100
    )

    cost: Decimal | None = Field(
        default=None,
        ge=0
    )

    notes: str | None = None


class TransportRead(TransportCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
