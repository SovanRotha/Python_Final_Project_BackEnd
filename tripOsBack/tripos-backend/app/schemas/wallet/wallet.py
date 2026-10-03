from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common.common import ResourceCreate


class WalletCreate(ResourceCreate):
    balance: Decimal = Field(default=Decimal("0"), ge=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)


class WalletRead(WalletCreate):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class WalletUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    data: dict = Field(default_factory=dict)
    balance: Decimal | None = Field(default=None, ge=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
