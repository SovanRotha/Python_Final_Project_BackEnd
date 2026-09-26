from sqlalchemy.orm import Session

from app.models.wallet import Wallet


def list_user_wallets(db: Session, user_id: int) -> list[Wallet]:
    return db.query(Wallet).filter(Wallet.user_id == user_id).all()