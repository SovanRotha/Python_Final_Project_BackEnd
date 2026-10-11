from fastapi import HTTPException, status
from sqlalchemy import true

from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.destination.destination import Destination
from app.core.config import settings


class DestinationController(ScopedResourceController):
    model = Destination
    resource_name = "Destination"

    def owner_filter(self):
        if self.user.email.casefold() in settings.admin_emails:
            return true()
        return super().owner_filter()

    def validate_update(self, resource, fields: dict) -> None:
        required = {"name", "country", "country_code"}
        if any(name in fields and fields[name] is None for name in required):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Destination name, country, and country_code cannot be null",
            )
