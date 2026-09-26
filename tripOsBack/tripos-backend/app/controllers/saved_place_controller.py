from app.controllers.resource_controller import ResourceController
from app.models.saved_place import SavedPlace


class SavedPlaceController(ResourceController):
    model = SavedPlace
    resource_name = "Saved place"