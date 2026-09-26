from app.controllers.expense_controller import ExpenseController
from app.routes.factory import create_resource_router

router = create_resource_router(ExpenseController, "expenses", "expenses")