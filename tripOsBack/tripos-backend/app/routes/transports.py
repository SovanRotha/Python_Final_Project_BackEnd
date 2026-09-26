from app.controllers.transport_controller import TransportController
from app.routes.factory import create_resource_router

router = create_resource_router(TransportController, "transports", "transports")