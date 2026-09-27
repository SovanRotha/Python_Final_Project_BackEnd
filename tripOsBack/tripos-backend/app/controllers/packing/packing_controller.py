from app.controllers.common.resource_controller import ResourceController
from app.models.packing.packing import PackingItem


class PackingController(ResourceController):
    model = PackingItem
    resource_name = "Packing item"
