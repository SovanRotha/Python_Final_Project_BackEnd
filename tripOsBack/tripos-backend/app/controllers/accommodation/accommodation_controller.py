from app.controllers.common.resource_controller import ResourceController
from app.models.accommodation.accommodation import Accommodation


class AccommodationController(ResourceController):
    model = Accommodation
    resource_name = "Accommodation"
