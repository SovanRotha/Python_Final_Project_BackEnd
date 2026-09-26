from app.core.database import Base
from app.models.base import ResourceMixin


class AIRequest(ResourceMixin, Base):
    __tablename__ = "ai_requests"