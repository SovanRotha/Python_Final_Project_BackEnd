from app.controllers.common.resource_controller import ResourceController
from app.models.screenshot.screenshot import Screenshot


class ScreenshotController(ResourceController):
    model = Screenshot
    resource_name = "Screenshot"
