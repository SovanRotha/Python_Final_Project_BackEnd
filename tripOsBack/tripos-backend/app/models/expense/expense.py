from datetime import date, datetime, timezone

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        index=True
    )

    trip_id = Column(
        BigInteger,
        ForeignKey("trips.id"),
        nullable=False,
        index=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    budget_category_id = Column(
        BigInteger,
        ForeignKey("budget_categories.id"),
        nullable=False,
        index=True
    )

    description = Column(
        String(255),
        nullable=False
    )

    amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    currency = Column(
        String(10),
        nullable=False
    )

    expense_date = Column(
        Date,
        nullable=False
    )

    payment_method = Column(
        String(100),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    trip = relationship(
        "Trip",
        back_populates="expenses"
    )

    user = relationship(
        "User",
        back_populates="expenses"
    )

    budget_category = relationship(
        "BudgetCategory",
        back_populates="expenses"
    )

    splits = relationship(
        "ExpenseSplit",
        back_populates="expense"
    )
