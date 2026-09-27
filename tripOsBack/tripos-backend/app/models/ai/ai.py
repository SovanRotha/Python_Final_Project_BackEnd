from app.core.database import Base
from app.models.common.base import ResourceMixin


class AIRequest(ResourceMixin, Base):
    __tablename__ = "ai_requests"
