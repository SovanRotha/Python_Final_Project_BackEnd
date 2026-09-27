from app.controllers.wallet.wallet_controller import WalletController
from app.routes.common.factory import create_resource_router

router = create_resource_router(WalletController, "wallets", "wallets")
