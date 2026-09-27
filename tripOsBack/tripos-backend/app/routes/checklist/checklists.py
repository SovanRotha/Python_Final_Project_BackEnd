from app.controllers.checklist.checklist_controller import ChecklistController
from app.routes.common.factory import create_resource_router

router = create_resource_router(ChecklistController, "checklists", "checklists")
