from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.expense.expense import Expense
from app.models.expense.expense_split import ExpenseSplit


class ExpenseSplitController(ScopedResourceController):
    model = ExpenseSplit
    resource_name = "Expense split"
    set_user_id = False

    def owner_filter(self):
        return ExpenseSplit.expense.has(Expense.user_id == self.user.id)

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Expense).filter(
                Expense.id == fields["expense_id"],
                Expense.user_id == self.user.id,
            ),
            "Expense",
        )