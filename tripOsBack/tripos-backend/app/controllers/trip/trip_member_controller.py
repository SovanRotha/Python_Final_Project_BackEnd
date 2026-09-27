from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.trip.trip import Trip
from app.models.trip.trip_member import TripMember


class TripMemberController(ScopedResourceController):
    model = TripMember
    resource_name = "Trip member"
    set_user_id = False

    def owner_filter(self):
        return TripMember.trip.has(Trip.user_id == self.user.id)

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Trip).filter(
                Trip.id == fields["trip_id"],
                Trip.user_id == self.user.id,
            ),
            "Trip",
        )