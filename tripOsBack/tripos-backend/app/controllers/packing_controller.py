from app.controllers.resource_controller import ResourceController
from app.models.packing import PackingItem


class PackingController(ResourceController):
    model = PackingItem
    resource_name = "Packing item"