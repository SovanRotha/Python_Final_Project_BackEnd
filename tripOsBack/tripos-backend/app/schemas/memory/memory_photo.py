from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MemoryPhotoCreate(BaseModel):
    memory_id: int

    image_path: str = Field(
        min_length=1,
        max_length=500
    )

    caption: str | None = Field(
        default=None,
        max_length=255
    )


class MemoryPhotoUpdate(BaseModel):
    image_path: str | None = Field(
        default=None,
        min_length=1,
        max_length=500
    )

    caption: str | None = Field(
        default=None,
        max_length=255
    )


class MemoryPhotoRead(MemoryPhotoCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
