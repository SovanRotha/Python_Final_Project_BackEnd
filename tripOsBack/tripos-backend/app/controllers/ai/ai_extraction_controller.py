from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.ai.ai_extraction import AIExtraction
from app.models.document.document import Document
from app.models.screenshot.screenshot import Screenshot
from app.models.trip.trip import Trip


class AIExtractionController(ScopedResourceController):
    model = AIExtraction
    resource_name = "AI extraction"

    def validate_create(self, fields: dict) -> None:
        trip_id = fields["trip_id"]
        self.require_owned(
            self.db.query(Trip).filter(
                Trip.id == trip_id,
                Trip.user_id == self.user.id,
            ),
            "Trip",
        )
        for model, field, label in (
            (Document, "document_id", "Document"),
            (Screenshot, "screenshot_id", "Screenshot"),
        ):
            resource_id = fields.get(field)
            if resource_id is not None:
                self.require_owned(
                    self.db.query(model).filter(
                        model.id == resource_id,
                        model.user_id == self.user.id,
                        model.trip_id == trip_id,
                    ),
                    label,
                )