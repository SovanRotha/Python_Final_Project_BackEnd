from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.reminder.reminder import ReminderType, ReminderStatus


class ReminderCreate(BaseModel):
    trip_id: int

    title: str = Field(
        min_length=1,
        max_length=255
    )

    description: str | None = None

    due_date: datetime

    type: ReminderType

    status: ReminderStatus = ReminderStatus.PENDING


class ReminderUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    description: str | None = None

    due_date: datetime | None = None

    type: ReminderType | None = None

    status: ReminderStatus | None = None


class ReminderRead(ReminderCreate):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
