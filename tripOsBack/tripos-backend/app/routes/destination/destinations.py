from app.controllers.destination.destination_controller import DestinationController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.destination.destination import (
	DestinationCreate,
	DestinationRead,
	DestinationUpdate,
)
from app.models.destination.destination import Destination

router = create_scoped_router(
	DestinationController,
	DestinationCreate,
	DestinationRead,
	"destinations",
	"destinations",
	update_schema=DestinationUpdate,
	public_read=True,
	public_filter=Destination.status == "published",
)
