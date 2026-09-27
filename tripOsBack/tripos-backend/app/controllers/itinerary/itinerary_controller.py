from app.controllers.common.resource_controller import ResourceController
from app.models.itinerary.itinerary import Itinerary


class ItineraryController(ResourceController):
    model = Itinerary
    resource_name = "Itinerary"
