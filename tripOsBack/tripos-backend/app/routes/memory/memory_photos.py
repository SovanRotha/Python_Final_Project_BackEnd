from app.controllers.memory.memory_photo_controller import MemoryPhotoController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.memory.memory_photo import (
    MemoryPhotoCreate,
    MemoryPhotoRead,
    MemoryPhotoUpdate,
)

router = create_scoped_router(
    MemoryPhotoController,
    MemoryPhotoCreate,
    MemoryPhotoRead,
    "memory-photos",
    "Memory photos",
    MemoryPhotoUpdate,
)