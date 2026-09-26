from app.controllers.resource_controller import ResourceController
from app.models.budget import Budget


class BudgetController(ResourceController):
    model = Budget
    resource_name = "Budget"