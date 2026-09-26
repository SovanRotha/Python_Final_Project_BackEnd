from app.controllers.resource_controller import ResourceController
from app.models.place import Place


class PlaceController(ResourceController):
    model = Place
    resource_name = "Place"