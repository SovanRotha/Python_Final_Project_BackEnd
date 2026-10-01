from app.controllers.notification.notification_controller import NotificationController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.notification.notification import (
    NotificationCreate,
    NotificationRead,
    NotificationUpdate,
)

router = create_scoped_router(
    NotificationController,
    NotificationCreate,
    NotificationRead,
    "notifications",
    "notifications",
    NotificationUpdate,
)
