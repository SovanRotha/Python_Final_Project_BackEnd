from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.destination.destination import Destination
from app.models.itinerary.itinerary_day import ItineraryDay
from app.models.itinerary.itinerary_item import ItineraryItem
from app.models.place.place import Place
from app.models.trip.trip import Trip


class ItineraryItemController(ScopedResourceController):
    model = ItineraryItem
    resource_name = "Itinerary item"
    set_user_id = False

    def owner_filter(self):
        return ItineraryItem.itinerary_day.has(
            ItineraryDay.trip.has(Trip.user_id == self.user.id)
        )

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(ItineraryDay).join(Trip).filter(
                ItineraryDay.id == fields["itinerary_day_id"],
                Trip.user_id == self.user.id,
            ),
            "Itinerary day",
        )
        place_id = fields.get("place_id")
        if place_id is not None:
            self.require_owned(
                self.db.query(Place).join(Destination).filter(
                    Place.id == place_id,
                    Destination.user_id == self.user.id,
                ),
                "Place",
            )