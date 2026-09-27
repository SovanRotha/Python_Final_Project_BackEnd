from app.controllers.checklist.checklist_item_controller import ChecklistItemController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.checklist.checklist_item import (
    ChecklistItemCreate,
    ChecklistItemRead,
    ChecklistItemUpdate,
)

router = create_scoped_router(
    ChecklistItemController,
    ChecklistItemCreate,
    ChecklistItemRead,
    "checklist-items",
    "Checklist items",
    ChecklistItemUpdate,
)