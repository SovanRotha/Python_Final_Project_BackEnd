from app.controllers.accommodation.accommodation_controller import AccommodationController
from app.routes.common.factory import create_resource_router

router = create_resource_router(AccommodationController, "accommodations", "accommodations")
