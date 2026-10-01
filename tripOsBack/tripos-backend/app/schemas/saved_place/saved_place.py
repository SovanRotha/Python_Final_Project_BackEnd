from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SavedPlaceCreate(BaseModel):
    place_id: int


class SavedPlaceRead(SavedPlaceCreate):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
