from app.controllers.itinerary.itinerary_item_controller import ItineraryItemController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.itinerary.itinerary_item import (
    ItineraryItemCreate,
    ItineraryItemRead,
    ItineraryItemUpdate,
)

router = create_scoped_router(
    ItineraryItemController,
    ItineraryItemCreate,
    ItineraryItemRead,
    "itinerary-items",
    "Itinerary items",
    ItineraryItemUpdate,
)