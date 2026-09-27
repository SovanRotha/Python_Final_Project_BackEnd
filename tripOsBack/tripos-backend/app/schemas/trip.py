from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.trip import TripStatus


class TripCreate(BaseModel):
    destination_id: int
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None

    start_date: date
    end_date: date

    currency: str = Field(min_length=3, max_length=10)

    budget_amount: Decimal | None = Field(
        default=None,
        ge=0
    )

    status: TripStatus = TripStatus.PLANNING

    cover_image: str | None = Field(
        default=None,
        max_length=500
    )


class TripUpdate(BaseModel):
    destination_id: int | None = None

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    description: str | None = None

    start_date: date | None = None
    end_date: date | None = None

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=10
    )

    budget_amount: Decimal | None = Field(
        default=None,
        ge=0
    )

    status: TripStatus | None = None

    cover_image: str | None = Field(
        default=None,
        max_length=500
    )


class TripRead(TripCreate):
    id: int
    user_id: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)