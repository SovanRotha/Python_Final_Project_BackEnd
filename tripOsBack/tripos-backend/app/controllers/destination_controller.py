from app.controllers.resource_controller import ResourceController
from app.models.destination import Destination


class DestinationController(ResourceController):
    model = Destination
    resource_name = "Destination"