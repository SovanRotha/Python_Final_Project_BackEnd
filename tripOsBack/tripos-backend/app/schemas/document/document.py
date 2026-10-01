from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentCreate(BaseModel):
    trip_id: int

    name: str = Field(
        min_length=1,
        max_length=255
    )

    type: str = Field(
        min_length=1,
        max_length=100
    )

    file_path: str = Field(
        min_length=1,
        max_length=500
    )

    expires_at: date | None = None


class DocumentUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    type: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    file_path: str | None = Field(
        default=None,
        min_length=1,
        max_length=500
    )

    expires_at: date | None = None


class DocumentRead(DocumentCreate):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
