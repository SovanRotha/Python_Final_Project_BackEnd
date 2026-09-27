from app.controllers.packing.packing_controller import PackingController
from app.routes.common.factory import create_resource_router

router = create_resource_router(PackingController, "packing", "packing")
