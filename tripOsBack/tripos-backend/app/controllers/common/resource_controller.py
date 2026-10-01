from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.common.base import ResourceMixin
from app.models.user.user import User


class ResourceController:
    model: type[ResourceMixin]
    resource_name = "Resource"

    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user

    def list(self):
        return self.db.query(self.model).filter(self.model.user_id == self.user.id).all()

    def create(self, fields: dict):
        values = dict(fields)
        model_fields = set(self.model.__table__.columns.keys())
        extra_fields = {
            key: values.pop(key)
            for key in tuple(values)
            if key not in model_fields and key != "user_id"
        }

        if extra_fields:
            values["data"] = {
                **values.get("data", {}),
                **jsonable_encoder(extra_fields),
            }

        values["user_id"] = self.user.id
        resource = self.model(**values)
        self.db.add(resource)
        self.db.commit()
        self.db.refresh(resource)
        return resource

    def get(self, resource_id: int):
        resource = self.db.query(self.model).filter(
            self.model.id == resource_id,
            self.model.user_id == self.user.id,
        ).first()
        if resource is None:
            raise HTTPException(status_code=404, detail=f"{self.resource_name} not found")
        return resource

    def delete(self, resource_id: int) -> None:
        resource = self.get(resource_id)
        self.db.delete(resource)
        self.db.commit()
