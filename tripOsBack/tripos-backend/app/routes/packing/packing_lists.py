from app.controllers.packing.packing_list_controller import PackingListController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.packing.packing_list import (
    PackingListCreate,
    PackingListRead,
    PackingListUpdate,
)

router = create_scoped_router(
    PackingListController,
    PackingListCreate,
    PackingListRead,
    "packing-lists",
    "Packing lists",
    PackingListUpdate,
)