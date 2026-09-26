from app.controllers.resource_controller import ResourceController
from app.models.screenshot import Screenshot


class ScreenshotController(ResourceController):
    model = Screenshot
    resource_name = "Screenshot"