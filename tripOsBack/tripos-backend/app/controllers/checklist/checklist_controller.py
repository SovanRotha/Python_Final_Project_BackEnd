from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.checklist.checklist import Checklist
from app.models.trip.trip import Trip


class ChecklistController(ScopedResourceController):
    model = Checklist
    resource_name = "Checklist"
    set_user_id = False

    def owner_filter(self):
        return Checklist.trip.has(Trip.user_id == self.user.id)

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Trip).filter(
                Trip.id == fields["trip_id"],
                Trip.user_id == self.user.id,
            ),
            "Trip",
        )
