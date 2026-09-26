from app.controllers.reminder_controller import ReminderController
from app.routes.factory import create_resource_router

router = create_resource_router(ReminderController, "reminders", "reminders")