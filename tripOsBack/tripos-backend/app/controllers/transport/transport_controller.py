from app.controllers.common.resource_controller import ResourceController
from app.models.transport.transport import Transport


class TransportController(ResourceController):
    model = Transport
    resource_name = "Transport"
