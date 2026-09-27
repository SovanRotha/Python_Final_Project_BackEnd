from app.controllers.common.resource_controller import ResourceController
from app.models.wallet.wallet import Wallet


class WalletController(ResourceController):
    model = Wallet
    resource_name = "Wallet"
