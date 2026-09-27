from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PackingListCreate(BaseModel):
    trip_id: int

    name: str = Field(
        min_length=1,
        max_length=255
    )


class PackingListUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )


class PackingListRead(PackingListCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
