from app.controllers.resource_controller import ResourceController
from app.models.wallet import Wallet


class WalletController(ResourceController):
    model = Wallet
    resource_name = "Wallet"