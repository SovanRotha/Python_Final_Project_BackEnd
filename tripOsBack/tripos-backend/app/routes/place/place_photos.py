from app.controllers.place.place_photo_controller import PlacePhotoController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.place.place_photo import PlacePhotoCreate, PlacePhotoRead

router = create_scoped_router(
    PlacePhotoController,
    PlacePhotoCreate,
    PlacePhotoRead,
    "place-photos",
    "Place photos",
)