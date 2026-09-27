from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AccommodationCreate(BaseModel):
    trip_id: int

    name: str = Field(
        min_length=1,
        max_length=255
    )

    address: str | None = None

    check_in: datetime
    check_out: datetime

    room_type: str | None = Field(
        default=None,
        max_length=100
    )

    confirmation_number: str | None = Field(
        default=None,
        max_length=255
    )

    cost: Decimal | None = Field(
        default=None,
        ge=0
    )

    notes: str | None = None


class AccommodationUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    address: str | None = None

    check_in: datetime | None = None
    check_out: datetime | None = None

    room_type: str | None = Field(
        default=None,
        max_length=100
    )

    confirmation_number: str | None = Field(
        default=None,
        max_length=255
    )

    cost: Decimal | None = Field(
        default=None,
        ge=0
    )

    notes: str | None = None


class AccommodationRead(AccommodationCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
