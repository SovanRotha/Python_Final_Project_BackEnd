from app.controllers.common.resource_controller import ResourceController
from app.models.reminder.reminder import Reminder


class ReminderController(ResourceController):
    model = Reminder
    resource_name = "Reminder"
