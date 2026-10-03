from app.controllers.destination.destination_controller import DestinationController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.destination.destination import DestinationCreate, DestinationRead

router = create_scoped_router(
	DestinationController,
	DestinationCreate,
	DestinationRead,
	"destinations",
	"destinations",
	public_read=True,
)
