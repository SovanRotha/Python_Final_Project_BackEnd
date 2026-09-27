from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.screenshot import ScreenshotType


class ScreenshotCreate(BaseModel):
    trip_id: int
    user_id: int

    title: str = Field(
        min_length=1,
        max_length=255
    )

    type: ScreenshotType

    image_path: str = Field(
        min_length=1,
        max_length=500
    )

    extracted_data: dict[str, Any] | None = None


class ScreenshotUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    type: ScreenshotType | None = None

    image_path: str | None = Field(
        default=None,
        min_length=1,
        max_length=500
    )

    extracted_data: dict[str, Any] | None = None


class ScreenshotRead(ScreenshotCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)