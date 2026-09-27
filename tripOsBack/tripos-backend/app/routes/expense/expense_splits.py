from app.controllers.expense.expense_split_controller import ExpenseSplitController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.expense.expense_split import (
    ExpenseSplitCreate,
    ExpenseSplitRead,
    ExpenseSplitUpdate,
)

router = create_scoped_router(
    ExpenseSplitController,
    ExpenseSplitCreate,
    ExpenseSplitRead,
    "expense-splits",
    "Expense splits",
    ExpenseSplitUpdate,
)