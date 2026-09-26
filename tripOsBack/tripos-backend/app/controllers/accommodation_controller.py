from app.controllers.resource_controller import ResourceController
from app.models.accommodation import Accommodation


class AccommodationController(ResourceController):
    model = Accommodation
    resource_name = "Accommodation"