from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.memory.memory import Memory
from app.models.memory.memory_photo import MemoryPhoto


class MemoryPhotoController(ScopedResourceController):
    model = MemoryPhoto
    resource_name = "Memory photo"
    set_user_id = False

    def owner_filter(self):
        return MemoryPhoto.memory.has(Memory.user_id == self.user.id)

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(Memory).filter(
                Memory.id == fields["memory_id"],
                Memory.user_id == self.user.id,
            ),
            "Memory",
        )