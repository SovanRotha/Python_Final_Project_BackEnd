from app.core.database import Base
from app.models.common.base import ResourceMixin


class PackingItem(ResourceMixin, Base):
    __tablename__ = "packing_items"
