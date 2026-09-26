from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class TripCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    data: dict = Field(default_factory=dict)
    start_date: date | None = None
    end_date: date | None = None
    status: str = "planned"


class TripRead(TripCreate):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)