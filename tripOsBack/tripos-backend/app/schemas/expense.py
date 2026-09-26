from datetime import date

from pydantic import ConfigDict, Field

from app.schemas.common import ResourceCreate


class ExpenseCreate(ResourceCreate):
    amount: float = Field(default=0, ge=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    category: str = "other"
    spent_on: date | None = None


class ExpenseRead(ExpenseCreate):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)