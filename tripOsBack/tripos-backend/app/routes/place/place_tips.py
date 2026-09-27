from app.controllers.place.place_tip_controller import PlaceTipController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.place.place_tip import PlaceTipCreate, PlaceTipRead, PlaceTipUpdate

router = create_scoped_router(
    PlaceTipController,
    PlaceTipCreate,
    PlaceTipRead,
    "place-tips",
    "Place tips",
    PlaceTipUpdate,
)