from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.destination.destination import Destination


class DestinationController(ScopedResourceController):
    model = Destination
    resource_name = "Destination"
