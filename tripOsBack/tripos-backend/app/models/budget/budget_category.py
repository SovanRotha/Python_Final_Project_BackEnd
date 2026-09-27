from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class BudgetCategory(Base):
    __tablename__ = "budget_categories"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        index=True
    )

    budget_id = Column(
        BigInteger,
        ForeignKey("budgets.id"),
        nullable=False,
        index=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    allocated_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    budget = relationship(
        "Budget",
        back_populates="categories"
    )

    expenses = relationship(
        "Expense",
        back_populates="budget_category"
    )
