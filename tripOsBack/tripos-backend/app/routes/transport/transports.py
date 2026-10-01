from app.controllers.transport.transport_controller import TransportController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.transport.transport import (
    TransportCreate,
    TransportRead,
    TransportUpdate,
)

router = create_scoped_router(
    TransportController,
    TransportCreate,
    TransportRead,
    "transports",
    "transports",
    TransportUpdate,
)
