from datetime import date

from sqlalchemy import Date, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import ResourceMixin


class Expense(ResourceMixin, Base):
    __tablename__ = "expenses"

    amount: Mapped[float] = mapped_column(Float, default=0)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    category: Mapped[str] = mapped_column(String(80), default="other")
    spent_on: Mapped[date | None] = mapped_column(Date, nullable=True)