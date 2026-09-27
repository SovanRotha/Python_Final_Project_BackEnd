from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.place.place_tip import PlaceTipType


class PlaceTipCreate(BaseModel):
    place_id: int

    title: str = Field(
        min_length=1,
        max_length=255
    )

    description: str = Field(
        min_length=1
    )

    type: PlaceTipType


class PlaceTipUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    description: str | None = Field(
        default=None,
        min_length=1
    )

    type: PlaceTipType | None = None


class PlaceTipRead(PlaceTipCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
