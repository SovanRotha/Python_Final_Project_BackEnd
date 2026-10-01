from app.controllers.checklist.checklist_controller import ChecklistController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.checklist.checklist import (
    ChecklistCreate,
    ChecklistRead,
    ChecklistUpdate,
)

router = create_scoped_router(
    ChecklistController,
    ChecklistCreate,
    ChecklistRead,
    "checklists",
    "checklists",
    ChecklistUpdate,
)
