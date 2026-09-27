from app.controllers.common.resource_controller import ResourceController
from app.models.place.place import Place


class PlaceController(ResourceController):
    model = Place
    resource_name = "Place"
