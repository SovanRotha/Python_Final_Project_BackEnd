from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ExpenseSplitCreate(BaseModel):
    expense_id: int
    user_id: int

    amount: Decimal = Field(
        gt=0
    )

    paid: bool = False


class ExpenseSplitUpdate(BaseModel):
    amount: Decimal | None = Field(
        default=None,
        gt=0
    )

    paid: bool | None = None


class ExpenseSplitRead(ExpenseSplitCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
