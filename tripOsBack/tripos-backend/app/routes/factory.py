from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.controllers.resource_controller import ResourceController
from app.core.database import get_db
from app.models.user import User
from app.schemas.common import ResourceCreate, ResourceRead


def create_resource_router(
    controller_type: type[ResourceController], path: str, tag: str
) -> APIRouter:
    router = APIRouter(prefix=f"/api/v1/{path}", tags=[tag])

    @router.get("", response_model=list[ResourceRead])
    def list_resources(
        db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
    ):
        return controller_type(db, current_user).list()

    @router.post("", response_model=ResourceRead, status_code=status.HTTP_201_CREATED)
    def create_resource(
        payload: ResourceCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        return controller_type(db, current_user).create(
            payload.model_dump(exclude_unset=True)
        )

    @router.get("/{resource_id}", response_model=ResourceRead)
    def get_resource(
        resource_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        return controller_type(db, current_user).get(resource_id)

    @router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_resource(
        resource_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> None:
        controller_type(db, current_user).delete(resource_id)

    return router