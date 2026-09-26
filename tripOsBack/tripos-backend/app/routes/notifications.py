from app.controllers.notification_controller import NotificationController
from app.routes.factory import create_resource_router

router = create_resource_router(NotificationController, "notifications", "notifications")