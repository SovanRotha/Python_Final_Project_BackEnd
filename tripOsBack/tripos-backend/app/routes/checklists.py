from app.controllers.checklist_controller import ChecklistController
from app.routes.factory import create_resource_router

router = create_resource_router(ChecklistController, "checklists", "checklists")