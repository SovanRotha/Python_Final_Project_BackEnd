from app.core.database import Base
from app.models.base import ResourceMixin


class Transport(ResourceMixin, Base):
    __tablename__ = "transports"