from app.controllers.resource_controller import ResourceController
from app.models.checklist import Checklist


class ChecklistController(ResourceController):
    model = Checklist
    resource_name = "Checklist"