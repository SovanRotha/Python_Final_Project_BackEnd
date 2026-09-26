from app.controllers.resource_controller import ResourceController
from app.models.trip import Trip


class TripController(ResourceController):
    model = Trip
    resource_name = "Trip"