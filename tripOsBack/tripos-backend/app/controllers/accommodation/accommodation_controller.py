from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.accommodation.accommodation import Accommodation
from app.models.trip.trip import Trip


class AccommodationController(ScopedResourceController):
    model = Accommodation
    resource_name = "Accommodation"
    set_user_id = False

    def owner_filter(self):
        return Accommodation.trip.has(Trip.user_id == self.user.id)

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Trip).filter(
                Trip.id == fields["trip_id"],
                Trip.user_id == self.user.id,
            ),
            "Trip",
        )
