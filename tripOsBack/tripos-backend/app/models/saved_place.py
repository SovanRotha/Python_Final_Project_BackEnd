from app.core.database import Base
from app.models.base import ResourceMixin


class SavedPlace(ResourceMixin, Base):
    __tablename__ = "saved_places"