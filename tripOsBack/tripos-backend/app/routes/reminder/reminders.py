from app.controllers.reminder.reminder_controller import ReminderController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.reminder.reminder import ReminderCreate, ReminderRead, ReminderUpdate

router = create_scoped_router(
    ReminderController,
    ReminderCreate,
    ReminderRead,
    "reminders",
    "reminders",
    ReminderUpdate,
)
