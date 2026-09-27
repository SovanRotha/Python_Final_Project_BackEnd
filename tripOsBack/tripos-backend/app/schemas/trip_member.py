from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.trip_member import TripMemberRole


class TripMemberCreate(BaseModel):
    trip_id: int
    user_id: int
    role: TripMemberRole = TripMemberRole.MEMBER


class TripMemberUpdate(BaseModel):
    role: TripMemberRole


class TripMemberRead(TripMemberCreate):
    id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)