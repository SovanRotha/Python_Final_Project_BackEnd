from app.controllers.document_controller import DocumentController
from app.routes.factory import create_resource_router

router = create_resource_router(DocumentController, "documents", "documents")