from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.budget.budget import Budget
from app.models.budget.budget_category import BudgetCategory
from app.models.trip.trip import Trip


class BudgetCategoryController(ScopedResourceController):
    model = BudgetCategory
    resource_name = "Budget category"
    set_user_id = False

    def owner_filter(self):
        return BudgetCategory.budget.has(
            Budget.trip.has(Trip.user_id == self.user.id)
        )

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Budget).join(Trip).filter(
                Budget.id == fields["budget_id"],
                Trip.user_id == self.user.id,
            ),
            "Budget",
        )