from app.controllers.resource_controller import ResourceController
from app.models.ai import AIRequest


class AIController(ResourceController):
    model = AIRequest
    resource_name = "AI request"