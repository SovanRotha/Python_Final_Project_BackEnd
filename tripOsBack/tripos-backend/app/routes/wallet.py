from app.controllers.wallet_controller import WalletController
from app.routes.factory import create_resource_router

router = create_resource_router(WalletController, "wallets", "wallets")