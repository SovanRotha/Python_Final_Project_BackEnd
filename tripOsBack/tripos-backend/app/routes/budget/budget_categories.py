from app.controllers.budget.budget_category_controller import BudgetCategoryController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.budget.budget_category import (
    BudgetCategoryCreate,
    BudgetCategoryRead,
    BudgetCategoryUpdate,
)

router = create_scoped_router(
    BudgetCategoryController,
    BudgetCategoryCreate,
    BudgetCategoryRead,
    "budget-categories",
    "Budget categories",
    BudgetCategoryUpdate,
)