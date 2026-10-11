from fastapi import HTTPException
from sqlalchemy import true

from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.destination.destination import Destination
from app.models.place.place import Place
from app.core.config import settings

class PlaceController(ScopedResourceController):
    model = Place
    resource_name = "Place"
    set_user_id = False

    def owner_filter(self):
        if self.user.email.casefold() in settings.admin_emails:
            return true()
        return Place.destination.has(Destination.user_id == self.user.id)

    def validate_create(self, fields: dict) -> None:
        if self.user.email.casefold() in settings.admin_emails:
            destination = self.db.get(Destination, fields["destination_id"])
            if destination is None:
                raise HTTPException(status_code=404, detail="Destination not found")
            return
        destination = self.db.query(Destination).filter(
            Destination.id == fields["destination_id"],
            Destination.user_id == self.user.id,
        ).first()
        if destination is None:
            raise HTTPException(status_code=404, detail="Destination not found")

    def validate_update(self, resource, fields: dict) -> None:
        required = {"name", "category"}
        if any(name in fields and fields[name] is None for name in required):
            raise HTTPException(
                status_code=422,
                detail="Place name and category cannot be null",
            )
        destination_id = fields.get("destination_id")
        if destination_id is None:
            return
        query = self.db.query(Destination).filter(Destination.id == destination_id)
        if self.user.email.casefold() not in settings.admin_emails:
            query = query.filter(Destination.user_id == self.user.id)
        if query.first() is None:
            raise HTTPException(status_code=404, detail="Destination not found")
