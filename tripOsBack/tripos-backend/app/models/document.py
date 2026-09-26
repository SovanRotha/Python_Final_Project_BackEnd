from app.core.database import Base
from app.models.base import ResourceMixin


class Document(ResourceMixin, Base):
    __tablename__ = "documents"