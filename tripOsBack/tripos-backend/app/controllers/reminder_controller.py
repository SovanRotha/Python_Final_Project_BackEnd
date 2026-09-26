from app.controllers.resource_controller import ResourceController
from app.models.reminder import Reminder


class ReminderController(ResourceController):
    model = Reminder
    resource_name = "Reminder"