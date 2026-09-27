from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.controllers.user.user_controller import UserController
from app.models.user.user import User
from app.schemas.user.user import UserRead

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return UserController(current_user).get_current_user()
