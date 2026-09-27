from app.controllers.trip.trip_member_controller import TripMemberController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.trip.trip_member import TripMemberCreate, TripMemberRead, TripMemberUpdate

router = create_scoped_router(
    TripMemberController,
    TripMemberCreate,
    TripMemberRead,
    "trip-members",
    "Trip members",
    TripMemberUpdate,
)