from app.controllers.document.document_controller import DocumentController
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.document.document import DocumentCreate, DocumentRead, DocumentUpdate

router = create_scoped_router(
    DocumentController,
    DocumentCreate,
    DocumentRead,
    "documents",
    "documents",
    DocumentUpdate,
)
