from app.controllers.transport.transport_controller import TransportController
from app.routes.common.factory import create_resource_router

router = create_resource_router(TransportController, "transports", "transports")
