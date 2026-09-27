from app.controllers.itinerary.itinerary_controller import ItineraryController
from app.routes.common.factory import create_resource_router

router = create_resource_router(ItineraryController, "itineraries", "itineraries")
