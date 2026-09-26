from pydantic import ConfigDict, Field

from app.schemas.common import ResourceCreate


class WalletCreate(ResourceCreate):
    balance: float = Field(default=0, ge=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)


class WalletRead(WalletCreate):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)