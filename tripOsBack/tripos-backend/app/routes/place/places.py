from app.controllers.place.place_controller import PlaceController
from app.schemas.place.place import PlaceCreate, PlaceRead
from app.routes.common.factory import create_resource_router

router = create_resource_router(
    PlaceController,
    "places",
    "places",
    create_schema=PlaceCreate,
    read_schema=PlaceRead,
    public_read=True,
)
