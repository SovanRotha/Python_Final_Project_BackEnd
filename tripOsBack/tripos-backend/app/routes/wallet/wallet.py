from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.controllers.wallet.wallet_controller import WalletController
from app.core.database import get_db
from app.models.user.user import User
from app.routes.common.factory import create_resource_router
from app.schemas.wallet.wallet import WalletCreate, WalletRead, WalletUpdate

router = create_resource_router(
    WalletController,
    "wallets",
    "wallets",
    create_schema=WalletCreate,
    read_schema=WalletRead,
)


@router.patch("/{wallet_id}", response_model=WalletRead)
def update_wallet(
    wallet_id: int,
    payload: WalletUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return WalletController(db, current_user).update(
        wallet_id,
        payload.model_dump(exclude_unset=True),
    )
