from app.controllers.memory.memory_controller import MemoryController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.memory.memory import MemoryCreate, MemoryRead, MemoryUpdate

router = create_scoped_router(
    MemoryController,
    MemoryCreate,
    MemoryRead,
    "memories",
    "memories",
    MemoryUpdate,
)
