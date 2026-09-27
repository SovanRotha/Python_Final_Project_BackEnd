from app.controllers.common.resource_controller import ResourceController
from app.models.memory.memory import Memory


class MemoryController(ResourceController):
    model = Memory
    resource_name = "Memory"
