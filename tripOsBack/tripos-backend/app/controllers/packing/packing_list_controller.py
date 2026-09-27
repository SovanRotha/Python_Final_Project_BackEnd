from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.packing.packing_list import PackingList
from app.models.trip.trip import Trip


class PackingListController(ScopedResourceController):
    model = PackingList
    resource_name = "Packing list"
    set_user_id = False

    def owner_filter(self):
        return PackingList.trip.has(Trip.user_id == self.user.id)

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Trip).filter(
                Trip.id == fields["trip_id"],
                Trip.user_id == self.user.id,
            ),
            "Trip",
        )