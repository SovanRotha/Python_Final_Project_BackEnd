from app.controllers.resource_controller import ResourceController
from app.models.document import Document


class DocumentController(ResourceController):
    model = Document
    resource_name = "Document"