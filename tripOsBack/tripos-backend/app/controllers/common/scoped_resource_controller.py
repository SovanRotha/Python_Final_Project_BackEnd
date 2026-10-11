from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.admin.audit_log import AdminAuditLog
from app.core.config import settings
from app.models.user.user import User


class ScopedResourceController:
    model: type
    resource_name = "Resource"
    set_user_id = True

    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user

    def owner_filter(self) -> Any:
        return self.model.user_id == self.user.id

    def validate_create(self, fields: dict) -> None:
        pass

    def validate_update(self, resource, fields: dict) -> None:
        pass

    def _audit_admin_action(
        self, action: str, resource_id: int | None
    ) -> None:
        if self.user.email.casefold() not in settings.admin_emails:
            return
        self.db.add(
            AdminAuditLog(
                actor_id=self.user.id,
                action=action,
                resource_type=self.resource_name.casefold(),
                resource_id=resource_id,
            )
        )

    def query_owned(self):
        return self.db.query(self.model).filter(self.owner_filter())

    def require_owned(self, query, resource_name: str):
        resource = query.first()
        if resource is None:
            raise HTTPException(status_code=404, detail=f"{resource_name} not found")
        return resource

    def list(self):
        return self.query_owned().all()

    def create(self, fields: dict):
        values = dict(fields)
        self.validate_create(values)
        if self.set_user_id:
            values["user_id"] = self.user.id
        resource = self.model(**values)
        self.db.add(resource)
        self.db.flush()
        self._audit_admin_action(f"{self.resource_name.casefold()}_created", resource.id)
        self.db.commit()
        self.db.refresh(resource)
        return resource

    def get(self, resource_id: int):
        return self.require_owned(
            self.query_owned().filter(self.model.id == resource_id),
            self.resource_name,
        )

    def update(self, resource_id: int, fields: dict):
        resource = self.get(resource_id)
        self.validate_update(resource, fields)
        for name, value in fields.items():
            setattr(resource, name, value)
        self._audit_admin_action(f"{self.resource_name.casefold()}_updated", resource.id)
        self.db.commit()
        self.db.refresh(resource)
        return resource

    def delete(self, resource_id: int) -> None:
        resource = self.get(resource_id)
        self._audit_admin_action(f"{self.resource_name.casefold()}_deleted", resource.id)
        self.db.delete(resource)
        self.db.commit()