from app.controllers.document.document_controller import DocumentController
from app.routes.common.factory import create_resource_router

router = create_resource_router(DocumentController, "documents", "documents")
