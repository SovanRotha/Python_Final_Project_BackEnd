from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.checklist.checklist import Checklist
from app.models.checklist.checklist_item import ChecklistItem
from app.models.trip.trip import Trip


class ChecklistItemController(ScopedResourceController):
    model = ChecklistItem
    resource_name = "Checklist item"
    set_user_id = False

    def owner_filter(self):
        return ChecklistItem.checklist.has(
            Checklist.trip.has(Trip.user_id == self.user.id)
        )

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Checklist).join(Trip).filter(
                Checklist.id == fields["checklist_id"],
                Trip.user_id == self.user.id,
            ),
            "Checklist",
        )