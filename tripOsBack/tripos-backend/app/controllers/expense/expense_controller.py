from fastapi import HTTPException

from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.budget.budget import Budget
from app.models.budget.budget_category import BudgetCategory
from app.models.expense.expense import Expense
from app.models.trip.trip import Trip


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
