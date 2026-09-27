from app.controllers.ai.ai_message_controller import AIMessageController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.ai.ai_message import AIMessageCreate, AIMessageRead, AIMessageUpdate

router = create_scoped_router(
    AIMessageController,
    AIMessageCreate,
    AIMessageRead,
    "ai/messages",
    "AI messages",
    AIMessageUpdate,
)