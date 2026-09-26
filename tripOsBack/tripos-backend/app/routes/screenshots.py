from app.controllers.screenshot_controller import ScreenshotController
from app.routes.factory import create_resource_router

router = create_resource_router(ScreenshotController, "screenshots", "screenshots")