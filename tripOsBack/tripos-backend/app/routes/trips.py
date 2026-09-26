from app.controllers.trip_controller import TripController
from app.routes.factory import create_resource_router

router = create_resource_router(TripController, "trips", "trips")