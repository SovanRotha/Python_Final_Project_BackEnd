from app.controllers.memory_controller import MemoryController
from app.routes.factory import create_resource_router

router = create_resource_router(MemoryController, "memories", "memories")