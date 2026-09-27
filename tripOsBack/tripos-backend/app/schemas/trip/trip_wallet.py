from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TripWalletCreate(BaseModel):
    trip_id: int

    target_amount: Decimal = Field(
        ge=0
    )

    current_amount: Decimal = Field(
        default=Decimal("0"),
        ge=0
    )

    currency: str = Field(
        min_length=3,
        max_length=10
    )


class TripWalletUpdate(BaseModel):
    target_amount: Decimal | None = Field(
        default=None,
        ge=0
    )

    current_amount: Decimal | None = Field(
        default=None,
        ge=0
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=10
    )


class TripWalletRead(TripWalletCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
