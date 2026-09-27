from app.controllers.screenshot.screenshot_controller import ScreenshotController
from app.routes.common.factory import create_resource_router

router = create_resource_router(ScreenshotController, "screenshots", "screenshots")
