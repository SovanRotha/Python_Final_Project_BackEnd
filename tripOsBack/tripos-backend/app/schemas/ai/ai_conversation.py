from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AIConversationCreate(BaseModel):
    user_id: int

    trip_id: int | None = None

    title: str = Field(
        min_length=1,
        max_length=255
    )


class AIConversationUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )


class AIConversationRead(AIConversationCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
