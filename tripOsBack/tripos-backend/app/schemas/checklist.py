from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChecklistCreate(BaseModel):
    trip_id: int

    title: str = Field(
        min_length=1,
        max_length=255
    )


class ChecklistUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )


class ChecklistRead(ChecklistCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)