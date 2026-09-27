from app.controllers.wallet.wallet_transaction_controller import WalletTransactionController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.wallet.wallet_transaction import (
    WalletTransactionCreate,
    WalletTransactionRead,
    WalletTransactionUpdate,
)

router = create_scoped_router(
    WalletTransactionController,
    WalletTransactionCreate,
    WalletTransactionRead,
    "wallet-transactions",
    "Wallet transactions",
    WalletTransactionUpdate,
)