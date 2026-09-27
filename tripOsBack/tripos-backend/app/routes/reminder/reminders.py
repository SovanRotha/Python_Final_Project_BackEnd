from app.controllers.reminder.reminder_controller import ReminderController
from app.routes.common.factory import create_resource_router

router = create_resource_router(ReminderController, "reminders", "reminders")
