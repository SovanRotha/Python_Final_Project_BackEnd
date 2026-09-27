from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ExpenseCreate(BaseModel):
    trip_id: int
    user_id: int
    budget_category_id: int | None = None

    description: str = Field(
        min_length=1,
        max_length=255
    )

    amount: Decimal = Field(
        gt=0
    )

    currency: str = Field(
        min_length=3,
        max_length=10
    )

    expense_date: date

    payment_method: str | None = Field(
        default=None,
        max_length=100
    )


class ExpenseUpdate(BaseModel):
    budget_category_id: int | None = None

    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    amount: Decimal | None = Field(
        default=None,
        gt=0
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=10
    )

    expense_date: date | None = None

    payment_method: str | None = Field(
        default=None,
        max_length=100
    )


class ExpenseRead(ExpenseCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)