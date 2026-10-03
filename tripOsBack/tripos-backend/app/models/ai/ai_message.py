from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class AIMessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class AIMessage(Base):
    __tablename__ = "ai_messages"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        index=True
    )

    conversation_id = Column(
        BigInteger,
        ForeignKey("ai_conversations.id"),
        nullable=False,
        index=True
    )

    role = Column(
        SQLEnum(
            AIMessageRole,
            name="ai_message_role"
        ),
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    conversation = relationship(
        "AIConversation",
        back_populates="messages"
    )
