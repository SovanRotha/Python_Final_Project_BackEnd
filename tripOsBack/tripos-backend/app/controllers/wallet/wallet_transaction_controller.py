from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.trip.trip import Trip
from app.models.trip.trip_wallet import TripWallet
from app.models.wallet.wallet_transaction import WalletTransaction


class WalletTransactionController(ScopedResourceController):
    model = WalletTransaction
    resource_name = "Wallet transaction"

    def owner_filter(self):
        return (
            (WalletTransaction.user_id == self.user.id)
            & WalletTransaction.wallet.has(
                TripWallet.trip.has(Trip.user_id == self.user.id)
            )
        )

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(TripWallet)
            .join(Trip)
            .filter(
                TripWallet.id == fields["wallet_id"],
                Trip.user_id == self.user.id,
            ),
            "Trip wallet",
        )