from fastapi import HTTPException
from sqlalchemy import func

from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.budget.budget import Budget
from app.models.budget.budget_category import BudgetCategory
from app.models.expense.expense import Expense
from app.models.trip.trip import Trip
from app.models.trip.trip_wallet import TripWallet
from app.controllers.wallet.wallet_transaction_controller import (
    WalletTransactionController,
)
from app.models.wallet.wallet_transaction import WalletTransaction
from app.models.wallet.wallet_transaction import WalletTransactionType


class ExpenseController(ScopedResourceController):
    model = Expense
    resource_name = "Expense"

    def validate_create(self, fields: dict) -> None:
        trip_id = fields["trip_id"]
        self._require_category(fields.get("budget_category_id"), trip_id)

    def validate_update(self, resource: Expense, fields: dict) -> None:
        if "budget_category_id" in fields:
            category_id = fields["budget_category_id"]
            if category_id is None:
                raise HTTPException(
                    status_code=422,
                    detail="An expense must have a budget category",
                )
            self._require_category(category_id, resource.trip_id)

    def _require_category(self, category_id: int | None, trip_id: int) -> None:
        if category_id is None:
            raise HTTPException(status_code=422, detail="A budget category is required")
        self.require_owned(
            self.db.query(BudgetCategory)
            .join(Budget)
            .join(Trip)
            .filter(
                BudgetCategory.id == category_id,
                Budget.trip_id == trip_id,
                Trip.user_id == self.user.id,
            ),
            "Budget category",
        )

    def _linked_transaction(self, expense_id: int):
        return (
            self.db.query(WalletTransaction)
            .filter(
                WalletTransaction.user_id == self.user.id,
                WalletTransaction.source == f"expense:{expense_id}",
            )
            .first()
        )

    def _refresh_budget_spent(self, trip_id: int) -> None:
        budget = self.db.query(Budget).filter(Budget.trip_id == trip_id).first()
        if budget is None:
            return
        total = (
            self.db.query(func.coalesce(func.sum(Expense.amount), 0))
            .filter(Expense.trip_id == trip_id)
            .scalar()
        )
        budget.spent_amount = total

    def create(self, fields: dict):
        values = dict(fields)
        wallet_id = values.pop("wallet_id", None)
        self.validate_create(values)

        if wallet_id is None:
            expense = Expense(user_id=self.user.id, **values)
            self.db.add(expense)
            self.db.flush()
            self._refresh_budget_spent(expense.trip_id)
            self.db.commit()
            self.db.refresh(expense)
            return expense

        wallet = self.require_owned(
            self.db.query(TripWallet)
            .join(Trip)
            .filter(
                TripWallet.id == wallet_id,
                TripWallet.trip_id == values["trip_id"],
                Trip.user_id == self.user.id,
            ),
            "Trip wallet",
        )
        if wallet.currency != values["currency"]:
            raise HTTPException(
                status_code=422,
                detail="Expense currency must match the trip wallet currency",
            )

        expense = Expense(user_id=self.user.id, **values)
        self.db.add(expense)
        self.db.flush()
        self._refresh_budget_spent(expense.trip_id)
        WalletTransactionController(self.db, self.user).create(
            {
                "wallet_id": wallet.id,
                "user_id": self.user.id,
                "type": WalletTransactionType.WITHDRAWAL,
                "amount": values["amount"],
                "source": f"expense:{expense.id}",
                "description": values["description"],
                "transaction_date": values["expense_date"],
            }
        )
        self.db.refresh(expense)
        return expense

    def update(self, resource_id: int, fields: dict):
        expense = self.get(resource_id)
        values = dict(fields)
        wallet_id = values.pop("wallet_id", None)
        self.validate_update(expense, values)
        transaction = self._linked_transaction(expense.id)

        wallet = None
        if wallet_id is not None and transaction is None:
            wallet = self.require_owned(
                self.db.query(TripWallet)
                .join(Trip)
                .filter(
                    TripWallet.id == wallet_id,
                    TripWallet.trip_id == expense.trip_id,
                    Trip.user_id == self.user.id,
                ),
                "Trip wallet",
            )
            new_currency = values.get("currency", expense.currency)
            if wallet.currency != new_currency:
                raise HTTPException(
                    status_code=422,
                    detail="Expense currency must match the trip wallet currency",
                )

        if transaction is not None:
            new_amount = values.get("amount", expense.amount)
            new_description = values.get("description", expense.description)
            new_date = values.get("expense_date", expense.expense_date)
            for name, value in values.items():
                setattr(expense, name, value)
            self.db.flush()
            self._refresh_budget_spent(expense.trip_id)
            WalletTransactionController(self.db, self.user).update(
                transaction.id,
                {
                    "amount": new_amount,
                    "description": new_description,
                    "transaction_date": new_date,
                },
            )
            self.db.refresh(expense)
            return expense

        for name, value in values.items():
            setattr(expense, name, value)
        self.db.flush()
        self._refresh_budget_spent(expense.trip_id)
        if wallet is not None:
            WalletTransactionController(self.db, self.user).create(
                {
                    "wallet_id": wallet.id,
                    "user_id": self.user.id,
                    "type": WalletTransactionType.WITHDRAWAL,
                    "amount": expense.amount,
                    "source": f"expense:{expense.id}",
                    "description": expense.description,
                    "transaction_date": expense.expense_date,
                }
            )
            self.db.refresh(expense)
            return expense

        self.db.commit()
        self.db.refresh(expense)
        return expense

    def delete(self, resource_id: int) -> None:
        expense = self.get(resource_id)
        transaction = self._linked_transaction(expense.id)
        trip_id = expense.trip_id
        self.db.delete(expense)
        self.db.flush()
        self._refresh_budget_spent(trip_id)
        if transaction is not None:
            WalletTransactionController(self.db, self.user).delete(transaction.id)
            return
        self.db.commit()
