from datetime import date as Date

from pydantic import BaseModel, ConfigDict, Field


class ItineraryDayCreate(BaseModel):
    trip_id: int
    day_number: int = Field(ge=1)
    date: Date
    title: str | None = Field(
        default=None,
        max_length=255
    )
    notes: str | None = None


class ItineraryDayUpdate(BaseModel):
    day_number: int | None = Field(
        default=None,
        ge=1
    )
    date: Date | None = None
    title: str | None = Field(
        default=None,
        max_length=255
    )
    notes: str | None = None


class ItineraryDayRead(ItineraryDayCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
