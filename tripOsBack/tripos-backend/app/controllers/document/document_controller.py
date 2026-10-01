from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.document.document import Document
from app.models.trip.trip import Trip


class DocumentController(ScopedResourceController):
    model = Document
    resource_name = "Document"

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Trip).filter(
                Trip.id == fields["trip_id"],
                Trip.user_id == self.user.id,
            ),
            "Trip",
        )
