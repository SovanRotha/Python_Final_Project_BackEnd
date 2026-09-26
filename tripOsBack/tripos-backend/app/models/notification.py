from app.core.database import Base
from app.models.base import ResourceMixin


class Notification(ResourceMixin, Base):
    __tablename__ = "notifications"