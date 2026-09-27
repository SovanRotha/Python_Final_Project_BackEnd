from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SavedPlaceCreate(BaseModel):
    user_id: int
    place_id: int


class SavedPlaceRead(SavedPlaceCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)