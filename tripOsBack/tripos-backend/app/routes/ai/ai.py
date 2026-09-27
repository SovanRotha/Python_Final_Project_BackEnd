from app.controllers.ai.ai_controller import AIController
from app.routes.common.factory import create_resource_router

router = create_resource_router(AIController, "ai/requests", "AI requests")
