from app.controllers.budget_controller import BudgetController
from app.routes.factory import create_resource_router

router = create_resource_router(BudgetController, "budgets", "budgets")