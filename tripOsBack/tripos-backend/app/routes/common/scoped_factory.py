from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.core.database import get_db
from app.models.user.user import User


def create_scoped_router(
    controller_type: type[ScopedResourceController],
    create_schema: type,
    read_schema: type,
    path: str,
    tag: str,
    update_schema: type | None = None,
) -> APIRouter:
    router = APIRouter(prefix=f"/api/v1/{path}", tags=[tag])

    @router.get("", response_model=list[read_schema])
    def list_resources(
        db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
    ):
        return controller_type(db, current_user).list()

    @router.post("", response_model=read_schema, status_code=status.HTTP_201_CREATED)
    def create_resource(
        payload: create_schema,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        return controller_type(db, current_user).create(
            payload.model_dump(exclude_unset=True)
        )

    @router.get("/{resource_id}", response_model=read_schema)
    def get_resource(
        resource_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        return controller_type(db, current_user).get(resource_id)

    if update_schema is not None:
        @router.patch("/{resource_id}", response_model=read_schema)
        def update_resource(
            resource_id: int,
            payload: update_schema,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user),
        ):
            return controller_type(db, current_user).update(
                resource_id,
                payload.model_dump(exclude_unset=True),
            )

    @router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_resource(
        resource_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> None:
        controller_type(db, current_user).delete(resource_id)

    return router