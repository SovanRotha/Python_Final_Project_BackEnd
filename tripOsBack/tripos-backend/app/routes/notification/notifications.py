from app.controllers.notification.notification_controller import NotificationController
from app.routes.common.factory import create_resource_router

router = create_resource_router(NotificationController, "notifications", "notifications")
