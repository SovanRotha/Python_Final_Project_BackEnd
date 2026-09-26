from app.core.database import Base
from app.models.base import ResourceMixin


class Accommodation(ResourceMixin, Base):
    __tablename__ = "accommodations"