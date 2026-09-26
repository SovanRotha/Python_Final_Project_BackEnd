from app.core.database import Base
from app.models.base import ResourceMixin


class Screenshot(ResourceMixin, Base):
    __tablename__ = "screenshots"