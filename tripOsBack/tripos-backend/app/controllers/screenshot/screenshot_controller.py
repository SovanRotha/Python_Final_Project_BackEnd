from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.screenshot.screenshot import Screenshot
from app.models.trip.trip import Trip


class ScreenshotController(ScopedResourceController):
    model = Screenshot
    resource_name = "Screenshot"

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Trip).filter(
                Trip.id == fields["trip_id"],
                Trip.user_id == self.user.id,
            ),
            "Trip",
        )
