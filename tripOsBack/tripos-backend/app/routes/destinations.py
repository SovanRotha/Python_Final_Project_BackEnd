from app.controllers.destination_controller import DestinationController
from app.routes.factory import create_resource_router

router = create_resource_router(DestinationController, "destinations", "destinations")