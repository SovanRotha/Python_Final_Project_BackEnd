from app.controllers.saved_place.saved_place_controller import SavedPlaceController
from app.routes.common.factory import create_resource_router

router = create_resource_router(SavedPlaceController, "saved-places", "saved places")
