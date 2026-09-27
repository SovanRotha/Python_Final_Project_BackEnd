from app.controllers.trip.trip_wallet_controller import TripWalletController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.trip.trip_wallet import TripWalletCreate, TripWalletRead, TripWalletUpdate

router = create_scoped_router(
    TripWalletController,
    TripWalletCreate,
    TripWalletRead,
    "trip-wallets",
    "Trip wallets",
    TripWalletUpdate,
)