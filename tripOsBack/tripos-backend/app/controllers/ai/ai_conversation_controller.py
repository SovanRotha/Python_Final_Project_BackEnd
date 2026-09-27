from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.ai.ai_conversation import AIConversation
from app.models.trip.trip import Trip


class AIConversationController(ScopedResourceController):
    model = AIConversation
    resource_name = "AI conversation"

    def validate_create(self, fields: dict) -> None:
        trip_id = fields.get("trip_id")
        if trip_id is not None:
            self.require_owned(
                self.db.query(Trip).filter(
                    Trip.id == trip_id,
                    Trip.user_id == self.user.id,
                ),
                "Trip",
            )