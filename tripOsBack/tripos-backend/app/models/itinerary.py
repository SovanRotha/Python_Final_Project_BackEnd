from app.core.database import Base
from app.models.base import ResourceMixin


class Itinerary(ResourceMixin, Base):
    __tablename__ = "itineraries"