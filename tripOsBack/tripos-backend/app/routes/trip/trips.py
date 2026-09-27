from app.controllers.trip.trip_controller import TripController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.trip.trip import TripCreate, TripRead, TripUpdate

router = create_scoped_router(
	TripController,
	TripCreate,
	TripRead,
	"trips",
	"trips",
	TripUpdate,
)
