from app.controllers.screenshot.screenshot_controller import ScreenshotController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.screenshot.screenshot import (
    ScreenshotCreate,
    ScreenshotRead,
    ScreenshotUpdate,
)

router = create_scoped_router(
    ScreenshotController,
    ScreenshotCreate,
    ScreenshotRead,
    "screenshots",
    "screenshots",
    ScreenshotUpdate,
)
