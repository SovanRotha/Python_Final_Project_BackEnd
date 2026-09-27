from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class PackingItem(Base):
    __tablename__ = "packing_items"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    packing_list_id = Column(
        BigInteger,
        ForeignKey("packing_lists.id"),
        nullable=False,
        index=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    category = Column(
        String(100),
        nullable=True
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1
    )

    is_packed = Column(
        Boolean,
        nullable=False,
        default=False
    )

    packing_list = relationship(
        "PackingList",
        back_populates="items"
    )