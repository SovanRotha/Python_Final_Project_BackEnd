from app.controllers.resource_controller import ResourceController
from app.models.memory import Memory


class MemoryController(ResourceController):
    model = Memory
    resource_name = "Memory"