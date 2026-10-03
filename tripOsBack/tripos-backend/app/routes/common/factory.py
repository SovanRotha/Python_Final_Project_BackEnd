from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.controllers.common.resource_controller import ResourceController
from app.core.database import get_db
from app.models.user.user import User
from app.schemas.common.common import ResourceCreate, ResourceRead


def create_resource_router(
    controller_type: type[ResourceController],
    path: str,
    tag: str,
    create_schema: type[BaseModel] = ResourceCreate,
    read_schema: type[BaseModel] = ResourceRead,
    public_read: bool = False,
) -> APIRouter:
    router = APIRouter(prefix=f"/api/v1/{path}", tags=[tag])

    if public_read:
        @router.get("", response_model=list[read_schema])
        def list_resources(db: Session = Depends(get_db)):
            return db.query(controller_type.model).all()

        @router.get("/{resource_id}", response_model=read_schema)
        def get_resource(resource_id: int, db: Session = Depends(get_db)):
            resource = db.get(controller_type.model, resource_id)
            if resource is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{controller_type.resource_name} not found",
                )
            return resource
    else:
        @router.get("", response_model=list[read_schema])
        def list_resources(
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user),
        ):
            return controller_type(db, current_user).list()

        @router.get("/{resource_id}", response_model=read_schema)
        def get_resource(
            resource_id: int,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user),
        ):
            return controller_type(db, current_user).get(resource_id)

    def create_resource(
        payload: BaseModel,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        return controller_type(db, current_user).create(payload.model_dump())

    create_resource.__annotations__["payload"] = create_schema
    router.post(
        "",
        response_model=read_schema,
        status_code=status.HTTP_201_CREATED,
    )(create_resource)

    @router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_resource(
        resource_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> None:
        controller_type(db, current_user).delete(resource_id)

    return router
