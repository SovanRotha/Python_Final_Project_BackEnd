from app.controllers.common.resource_controller import ResourceController
from app.models.notification.notification import Notification


class NotificationController(ResourceController):
    model = Notification
    resource_name = "Notification"
