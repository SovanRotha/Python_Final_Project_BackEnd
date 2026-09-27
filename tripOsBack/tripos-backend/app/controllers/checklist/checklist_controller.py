from app.controllers.common.resource_controller import ResourceController
from app.models.checklist.checklist import Checklist


class ChecklistController(ResourceController):
    model = Checklist
    resource_name = "Checklist"
