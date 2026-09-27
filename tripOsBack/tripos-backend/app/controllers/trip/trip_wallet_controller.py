from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.trip.trip import Trip
from app.models.trip.trip_wallet import TripWallet


class TripWalletController(ScopedResourceController):
    model = TripWallet
    resource_name = "Trip wallet"
    set_user_id = False

    def owner_filter(self):
        return TripWallet.trip.has(Trip.user_id == self.user.id)

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Trip).filter(
                Trip.id == fields["trip_id"],
                Trip.user_id == self.user.id,
            ),
            "Trip",
        )