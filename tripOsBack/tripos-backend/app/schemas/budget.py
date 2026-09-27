from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BudgetCreate(BaseModel):
    trip_id: int

    total_budget: Decimal = Field(
        ge=0
    )

    saved_amount: Decimal = Field(
        default=Decimal("0"),
        ge=0
    )

    spent_amount: Decimal = Field(
        default=Decimal("0"),
        ge=0
    )

    currency: str = Field(
        min_length=3,
        max_length=10
    )


class BudgetUpdate(BaseModel):
    total_budget: Decimal | None = Field(
        default=None,
        ge=0
    )

    saved_amount: Decimal | None = Field(
        default=None,
        ge=0
    )

    spent_amount: Decimal | None = Field(
        default=None,
        ge=0
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=10
    )


class BudgetRead(BudgetCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)