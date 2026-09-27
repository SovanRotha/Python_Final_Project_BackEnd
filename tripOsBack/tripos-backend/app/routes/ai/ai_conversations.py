from app.controllers.ai.ai_conversation_controller import AIConversationController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.ai.ai_conversation import (
    AIConversationCreate,
    AIConversationRead,
    AIConversationUpdate,
)

router = create_scoped_router(
    AIConversationController,
    AIConversationCreate,
    AIConversationRead,
    "ai/conversations",
    "AI conversations",
    AIConversationUpdate,
)