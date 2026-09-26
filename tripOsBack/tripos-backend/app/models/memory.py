from app.core.database import Base
from app.models.base import ResourceMixin


class Memory(ResourceMixin, Base):
    __tablename__ = "memories"