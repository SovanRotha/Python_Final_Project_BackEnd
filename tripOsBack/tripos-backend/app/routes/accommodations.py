from app.controllers.accommodation_controller import AccommodationController
from app.routes.factory import create_resource_router

router = create_resource_router(AccommodationController, "accommodations", "accommodations")