from app.controllers.common.resource_controller import ResourceController
from app.models.wallet.wallet import Wallet


class WalletController(ResourceController):
    model = Wallet
    resource_name = "Wallet"

    def update(self, resource_id: int, fields: dict):
        wallet = self.get(resource_id)
        for name, value in fields.items():
            if value is not None or name == "description":
                setattr(wallet, name, value)
        self.db.commit()
        self.db.refresh(wallet)
        return wallet
