from app.controllers.place.place_controller import PlaceController
from app.routes.common.factory import create_resource_router

router = create_resource_router(PlaceController, "places", "places")
