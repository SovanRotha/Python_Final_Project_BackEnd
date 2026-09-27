from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.destination.destination import Destination
from app.models.place.place import Place
from app.models.place.place_tip import PlaceTip


class PlaceTipController(ScopedResourceController):
    model = PlaceTip
    resource_name = "Place tip"
    set_user_id = False

    def owner_filter(self):
        return PlaceTip.place.has(
            Place.destination.has(Destination.user_id == self.user.id)
        )

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Place).join(Destination).filter(
                Place.id == fields["place_id"],
                Destination.user_id == self.user.id,
            ),
            "Place",
        )