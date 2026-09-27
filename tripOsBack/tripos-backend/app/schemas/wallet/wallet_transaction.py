from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.wallet.wallet_transaction import WalletTransactionType


class WalletTransactionCreate(BaseModel):
    wallet_id: int
    user_id: int

    type: WalletTransactionType

    amount: Decimal = Field(
        gt=0
    )

    source: str | None = Field(
        default=None,
        max_length=255
    )

    description: str | None = None

    transaction_date: date


class WalletTransactionUpdate(BaseModel):
    type: WalletTransactionType | None = None

    amount: Decimal | None = Field(
        default=None,
        gt=0
    )

    source: str | None = Field(
        default=None,
        max_length=255
    )

    description: str | None = None

    transaction_date: date | None = None


class WalletTransactionRead(WalletTransactionCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
