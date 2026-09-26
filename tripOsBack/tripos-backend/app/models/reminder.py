from app.core.database import Base
from app.models.base import ResourceMixin


class Reminder(ResourceMixin, Base):
    __tablename__ = "reminders"