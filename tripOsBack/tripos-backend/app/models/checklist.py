from app.core.database import Base
from app.models.base import ResourceMixin


class Checklist(ResourceMixin, Base):
    __tablename__ = "checklists"