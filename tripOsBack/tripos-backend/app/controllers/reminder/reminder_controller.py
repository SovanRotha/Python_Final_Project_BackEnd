from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.reminder.reminder import Reminder
from app.models.trip.trip import Trip


class ReminderController(ScopedResourceController):
    model = Reminder
    resource_name = "Reminder"

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Trip).filter(
                Trip.id == fields["trip_id"],
                Trip.user_id == self.user.id,
            ),
            "Trip",
        )
