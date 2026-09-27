from app.core.database import Base
from app.models.common.base import ResourceMixin


class Itinerary(ResourceMixin, Base):
    __tablename__ = "itineraries"
