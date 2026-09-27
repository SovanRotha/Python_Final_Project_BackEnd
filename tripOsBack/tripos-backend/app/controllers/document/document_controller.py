from app.controllers.common.resource_controller import ResourceController
from app.models.document.document import Document


class DocumentController(ResourceController):
    model = Document
    resource_name = "Document"
