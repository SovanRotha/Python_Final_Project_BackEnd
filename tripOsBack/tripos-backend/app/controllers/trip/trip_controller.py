from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.destination.destination import Destination
from app.models.trip.trip import Trip


class TripController(ScopedResourceController):
    model = Trip
    resource_name = "Trip"

    def validate_create(self, fields: dict) -> None:
        self._validate_destination(fields.get("destination_id"))

    def validate_update(self, resource: Trip, fields: dict) -> None:
        if "destination_id" in fields:
            self._validate_destination(fields["destination_id"])

    def _validate_destination(self, destination_id: int | None) -> None:
        self.require_owned(
            self.db.query(Destination).filter(
                Destination.id == destination_id,
                Destination.user_id == self.user.id,
            ),
            "Destination",
        )
