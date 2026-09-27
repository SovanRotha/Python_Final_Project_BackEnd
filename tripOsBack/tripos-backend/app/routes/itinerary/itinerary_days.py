from app.controllers.itinerary.itinerary_day_controller import ItineraryDayController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.itinerary.itinerary_day import (
    ItineraryDayCreate,
    ItineraryDayRead,
    ItineraryDayUpdate,
)

router = create_scoped_router(
    ItineraryDayController,
    ItineraryDayCreate,
    ItineraryDayRead,
    "itinerary-days",
    "Itinerary days",
    ItineraryDayUpdate,
)