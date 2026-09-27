from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BudgetCategoryCreate(BaseModel):
    budget_id: int

    name: str = Field(
        min_length=1,
        max_length=255
    )

    allocated_amount: Decimal = Field(
        ge=0
    )


class BudgetCategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    allocated_amount: Decimal | None = Field(
        default=None,
        ge=0
    )


class BudgetCategoryRead(BudgetCategoryCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
