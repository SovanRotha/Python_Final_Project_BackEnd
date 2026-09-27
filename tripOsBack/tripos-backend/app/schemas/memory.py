from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class MemoryCreate(BaseModel):
    trip_id: int
    user_id: int

    title: str = Field(
        min_length=1,
        max_length=255
    )

    description: str | None = None

    memory_date: date

    location: str | None = Field(
        default=None,
        max_length=255
    )


class MemoryUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    description: str | None = None

    memory_date: date | None = None

    location: str | None = Field(
        default=None,
        max_length=255
    )


class MemoryRead(MemoryCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)