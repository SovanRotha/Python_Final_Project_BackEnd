from app.controllers.place_controller import PlaceController
from app.routes.factory import create_resource_router

router = create_resource_router(PlaceController, "places", "places")