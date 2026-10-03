from decimal import Decimal

from fastapi import HTTPException

from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.trip.trip import Trip
from app.models.trip.trip_wallet import TripWallet
from app.models.wallet.wallet_transaction import (
    WalletTransaction,
    WalletTransactionType,
)


class WalletTransactionController(ScopedResourceController):
    model = WalletTransaction
    resource_name = "Wallet transaction"

    def owner_filter(self):
        return WalletTransaction.wallet.has(
            TripWallet.trip.has(Trip.user_id == self.user.id)
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

    @staticmethod
    def _signed_amount(transaction_type, amount) -> Decimal:
        value = Decimal(str(amount))
        return (
            value
            if transaction_type == WalletTransactionType.DEPOSIT
            else -value
        )

    def _apply_balance_change(
        self,
        wallet: TripWallet,
        old_type,
        old_amount,
        new_type,
        new_amount,
    ) -> None:
        change = Decimal("0")
        if old_type is not None and old_amount is not None:
            change -= self._signed_amount(old_type, old_amount)
        if new_type is not None and new_amount is not None:
            change += self._signed_amount(new_type, new_amount)

        updated_balance = Decimal(str(wallet.current_amount)) + change
        if updated_balance < 0:
            raise HTTPException(
                status_code=422,
                detail="Insufficient trip wallet funds for this transaction",
            )
        wallet.current_amount = updated_balance

    def create(self, fields: dict):
        values = dict(fields)
        self.validate_create(values)
        wallet = self.db.query(TripWallet).filter(
            TripWallet.id == values["wallet_id"]
        ).first()
        self._apply_balance_change(
            wallet,
            None,
            None,
            values["type"],
            values["amount"],
        )
        values["user_id"] = self.user.id
        transaction = self.model(**values)
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def update(self, resource_id: int, fields: dict):
        transaction = self.get(resource_id)
        wallet = self.db.query(TripWallet).filter(
            TripWallet.id == transaction.wallet_id
        ).first()
        self._apply_balance_change(
            wallet,
            transaction.type,
            transaction.amount,
            fields.get("type", transaction.type),
            fields.get("amount", transaction.amount),
        )
        for name, value in fields.items():
            if value is not None:
                setattr(transaction, name, value)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def delete(self, resource_id: int) -> None:
        transaction = self.get(resource_id)
        wallet = self.db.query(TripWallet).filter(
            TripWallet.id == transaction.wallet_id
        ).first()
        self._apply_balance_change(
            wallet,
            transaction.type,
            transaction.amount,
            None,
            None,
        )
        self.db.delete(transaction)
        self.db.commit()