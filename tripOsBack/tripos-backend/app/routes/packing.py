from app.controllers.packing_controller import PackingController
from app.routes.factory import create_resource_router

router = create_resource_router(PackingController, "packing", "packing")