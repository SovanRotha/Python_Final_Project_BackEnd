from app.controllers.accommodation.accommodation_controller import AccommodationController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.accommodation.accommodation import (
    AccommodationCreate,
    AccommodationRead,
    AccommodationUpdate,
)

router = create_scoped_router(
    AccommodationController,
    AccommodationCreate,
    AccommodationRead,
    "accommodations",
    "accommodations",
    AccommodationUpdate,
)
