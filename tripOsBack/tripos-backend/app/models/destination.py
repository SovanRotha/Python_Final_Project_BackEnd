from app.core.database import Base
from app.models.base import ResourceMixin


class Destination(ResourceMixin, Base):
    __tablename__ = "destinations"