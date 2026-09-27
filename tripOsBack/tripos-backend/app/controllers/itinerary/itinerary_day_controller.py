from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.itinerary.itinerary_day import ItineraryDay
from app.models.trip.trip import Trip


class ItineraryDayController(ScopedResourceController):
    model = ItineraryDay
    resource_name = "Itinerary day"
    set_user_id = False

    def owner_filter(self):
        return ItineraryDay.trip.has(Trip.user_id == self.user.id)

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Trip).filter(
                Trip.id == fields["trip_id"],
                Trip.user_id == self.user.id,
            ),
            "Trip",
        )