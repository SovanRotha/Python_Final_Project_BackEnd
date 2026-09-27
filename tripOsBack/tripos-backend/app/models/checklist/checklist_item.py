from datetime import date

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    ForeignKey,
    String,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class ChecklistItem(Base):
    __tablename__ = "checklist_items"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    checklist_id = Column(
        BigInteger,
        ForeignKey("checklists.id"),
        nullable=False,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    due_date = Column(
        Date,
        nullable=True
    )

    is_completed = Column(
        Boolean,
        nullable=False,
        default=False
    )

    checklist = relationship(
        "Checklist",
        back_populates="items"
    )
