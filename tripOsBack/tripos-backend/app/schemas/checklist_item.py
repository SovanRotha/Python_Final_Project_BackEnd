from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ChecklistItemCreate(BaseModel):
    checklist_id: int

    title: str = Field(
        min_length=1,
        max_length=255
    )

    due_date: date | None = None

    is_completed: bool = False


class ChecklistItemUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    due_date: date | None = None

    is_completed: bool | None = None


class ChecklistItemRead(ChecklistItemCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)