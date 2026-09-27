from app.controllers.ai.ai_extraction_controller import AIExtractionController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.ai.ai_extraction import (
    AIExtractionCreate,
    AIExtractionRead,
    AIExtractionUpdate,
)

router = create_scoped_router(
    AIExtractionController,
    AIExtractionCreate,
    AIExtractionRead,
    "ai/extractions",
    "AI extractions",
    AIExtractionUpdate,
)