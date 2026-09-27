from datetime import date, datetime, timezone
from enum import Enum

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class WalletTransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    wallet_id = Column(
        BigInteger,
        ForeignKey("trip_wallets.id"),
        nullable=False,
        index=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    type = Column(
        SQLEnum(
            WalletTransactionType,
            name="wallet_transaction_type"
        ),
        nullable=False
    )

    amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    source = Column(
        String(255),
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )

    transaction_date = Column(
        Date,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    wallet = relationship(
        "TripWallet",
        back_populates="transactions"
    )

    user = relationship(
        "User",
        back_populates="wallet_transactions"
    )
