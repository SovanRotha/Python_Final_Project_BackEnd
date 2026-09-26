from app.core.database import Base
from app.models.base import ResourceMixin


class Place(ResourceMixin, Base):
    __tablename__ = "places"