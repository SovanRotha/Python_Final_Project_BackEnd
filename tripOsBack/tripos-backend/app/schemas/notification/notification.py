from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NotificationCreate(BaseModel):
    user_id: int

    trip_id: int | None = None
    reminder_id: int | None = None

    title: str = Field(
        min_length=1,
        max_length=255
    )

    message: str = Field(
        min_length=1
    )

    type: str = Field(
        min_length=1,
        max_length=100
    )

    is_read: bool = False


class NotificationUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    message: str | None = Field(
        default=None,
        min_length=1
    )

    type: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    is_read: bool | None = None


class NotificationRead(NotificationCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
