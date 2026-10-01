from fastapi import HTTPException

from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.destination.destination import Destination
from app.models.place.place import Place

class PlaceController(ScopedResourceController):
    model = Place
    resource_name = "Place"
    set_user_id = False

    def owner_filter(self):
        return Place.destination.has(Destination.user_id == self.user.id)

    def validate_create(self, fields: dict) -> None:
        destination = self.db.query(Destination).filter(
            Destination.id == fields["destination_id"],
            Destination.user_id == self.user.id,
        ).first()
        if destination is None:
            raise HTTPException(status_code=404, detail="Destination not found")
