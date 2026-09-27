from app.controllers.expense.expense_controller import ExpenseController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.expense.expense import ExpenseCreate, ExpenseRead, ExpenseUpdate

router = create_scoped_router(
	ExpenseController,
	ExpenseCreate,
	ExpenseRead,
	"expenses",
	"expenses",
	ExpenseUpdate,
)
