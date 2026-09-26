from app.controllers.resource_controller import ResourceController
from app.models.expense import Expense


class ExpenseController(ResourceController):
    model = Expense
    resource_name = "Expense"