from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class ExpenseSplit(Base):
    __tablename__ = "expense_splits"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    expense_id = Column(
        BigInteger,
        ForeignKey("expenses.id"),
        nullable=False,
        index=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    paid = Column(
        Boolean,
        nullable=False,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    expense = relationship(
        "Expense",
        back_populates="splits"
    )

    user = relationship(
        "User",
        back_populates="expense_splits"
    )
