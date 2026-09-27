from app.controllers.memory.memory_controller import MemoryController
from app.routes.common.factory import create_resource_router

router = create_resource_router(MemoryController, "memories", "memories")
