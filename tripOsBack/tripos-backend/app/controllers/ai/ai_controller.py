from app.controllers.common.resource_controller import ResourceController
from app.models.ai.ai import AIRequest


class AIController(ResourceController):
    model = AIRequest
    resource_name = "AI request"
