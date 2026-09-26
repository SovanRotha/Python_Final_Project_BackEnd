from app.controllers.resource_controller import ResourceController
from app.models.itinerary import Itinerary


class ItineraryController(ResourceController):
    model = Itinerary
    resource_name = "Itinerary"