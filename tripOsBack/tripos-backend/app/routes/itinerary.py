from app.controllers.itinerary_controller import ItineraryController
from app.routes.factory import create_resource_router

router = create_resource_router(ItineraryController, "itineraries", "itineraries")