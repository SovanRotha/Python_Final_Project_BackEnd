from datetime import datetime, time
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.itinerary_item import ItineraryItemType, ItineraryItemStatus


class ItineraryItemCreate(BaseModel):
    itinerary_day_id: int
    place_id: int | None = None

    title: str = Field(
        min_length=1,
        max_length=255
    )

    description: str | None = None

    start_time: time | None = None
    end_time: time | None = None

    estimated_cost: Decimal | None = Field(
        default=None,
        ge=0
    )

    type: ItineraryItemType
    status: ItineraryItemStatus = ItineraryItemStatus.PLANNED

    order_index: int = Field(
        default=0,
        ge=0
    )


class ItineraryItemUpdate(BaseModel):
    place_id: int | None = None

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    description: str | None = None

    start_time: time | None = None
    end_time: time | None = None

    estimated