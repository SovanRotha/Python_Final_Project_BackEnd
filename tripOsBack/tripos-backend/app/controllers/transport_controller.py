from app.controllers.resource_controller import ResourceController
from app.models.transport import Transport


class TransportController(ResourceController):
    model = Transport
    resource_name = "Transport"