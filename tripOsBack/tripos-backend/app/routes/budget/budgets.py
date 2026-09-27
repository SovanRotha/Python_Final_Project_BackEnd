from app.controllers.budget.budget_controller import BudgetController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.budget.budget import BudgetCreate, BudgetRead, BudgetUpdate

router = create_scoped_router(
	BudgetController,
	BudgetCreate,
	BudgetRead,
	"budgets",
	"budgets",
	BudgetUpdate,
)
