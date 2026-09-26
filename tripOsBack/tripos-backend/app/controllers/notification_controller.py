from app.controllers.resource_controller import ResourceController
from app.models.notification import Notification


class NotificationController(ResourceController):
    model = Notification
    resource_name = "Notification"