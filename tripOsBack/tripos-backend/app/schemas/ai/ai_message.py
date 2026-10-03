from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.ai.ai_message import AIMessageRole


class AIMessageCreate(BaseModel):
    conversation_id: int

    role: AIMessageRole

    message: str = Field(
        min_length=1
    )


class AIMessageUpdate(BaseModel):
    message: str = Field(
        min_length=1
    )


class AIMessageRead(AIMessageCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AIChatSendRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)


class AIChatSendResponse(BaseModel):
    user_message: AIMessageRead
    assistant_message: AIMessageRead
