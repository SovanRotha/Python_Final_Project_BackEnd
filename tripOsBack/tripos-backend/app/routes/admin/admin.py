from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.controllers.admin.admin_controller import AdminController
from app.core.database import get_db
from app.models.user.user import User

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.get("/users/count")
def count_users(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return {"count": AdminController(db).count_users()}
