from fastapi import Depends
from sqlalchemy.orm import Session

from app.controllers.place.place_controller import PlaceController
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user.user import User
from app.schemas.place.place import PlaceCreate, PlaceRead, PlaceUpdate
from app.routes.common.factory import create_resource_router

router = create_resource_router(
    PlaceController,
    "places",
    "places",
    create_schema=PlaceCreate,
    read_schema=PlaceRead,
    public_read=True,
)


@router.patch("/{resource_id}", response_model=PlaceRead)
def update_place(
    resource_id: int,
    payload: PlaceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PlaceController(db, current_user).update(
        resource_id, payload.model_dump(exclude_unset=True)
    )
