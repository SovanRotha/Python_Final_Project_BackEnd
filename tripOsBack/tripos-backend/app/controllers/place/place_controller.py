from app.controllers.common.resource_controller import ResourceController
from app.models.place.place import Place
from app.controllers.common.scoped_resource_controller import ScopedResourceController

class PlaceController(ScopedResourceController):
    model = Place
    resource_name = "Place"
