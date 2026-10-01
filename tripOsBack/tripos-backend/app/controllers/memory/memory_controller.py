from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.memory.memory import Memory
from app.models.trip.trip import Trip


class MemoryController(ScopedResourceController):
    model = Memory
    resource_name = "Memory"

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Trip).filter(
                Trip.id == fields["trip_id"],
                Trip.user_id == self.user.id,
            ),
            "Trip",
        )
