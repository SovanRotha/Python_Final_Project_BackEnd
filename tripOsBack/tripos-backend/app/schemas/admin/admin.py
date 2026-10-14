from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.destination.destination import (
    DestinationCreate,
    DestinationStatus,
    DestinationUpdate,
)
from app.schemas.trip.trip import TripRead


class AdminUserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    status: bool | None
    is_admin: bool
    created_at: datetime
    trip_count: int


class AdminUserStatusUpdate(BaseModel):
    status: bool


class AdminTripOwnerRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    status: bool | None

    model_config = ConfigDict(from_attributes=True)


class AdminTripRead(TripRead):
    user: AdminTripOwnerRead


class AdminDestinationCreate(DestinationCreate):
    status: DestinationStatus = DestinationStatus.DRAFT


class AdminDestinationUpdate(DestinationUpdate):
    pass


class AdminDestinationStatusUpdate(BaseModel):
    status: DestinationStatus


class ReportCreate(BaseModel):
    reason: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=5000)
    resource_type: str | None = Field(default=None, max_length=50)
    resource_id: int | None = Field(default=None, ge=1)


class ReportStatus(str, Enum):
    OPEN = "open"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class ReportReview(BaseModel):
    status: ReportStatus
    resolution: str | None = Field(default=None, max_length=5000)


class AdminReportRead(BaseModel):
    id: int
    user_id: int
    reason: str
    description: str
    resource_type: str | None
    resource_id: int | None
    status: ReportStatus
    resolution: str | None
    reviewed_by_id: int | None
    reviewed_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AdminAuditLogRead(BaseModel):
    id: int
    actor_id: int | None
    action: str
    resource_type: str
    resource_id: int | None
    details: dict
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
