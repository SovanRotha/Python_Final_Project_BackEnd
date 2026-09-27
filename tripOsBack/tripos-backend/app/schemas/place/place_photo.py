from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PlacePhotoCreate(BaseModel):
    place_id: int

    image_path: str = Field(
        min_length=1,
        max_length=500
    )

    caption: str | None = Field(
        default=None,
        max_length=255
    )


class PlacePhotoRead(PlacePhotoCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
