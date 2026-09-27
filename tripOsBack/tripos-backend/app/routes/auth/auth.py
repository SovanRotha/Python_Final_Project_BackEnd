from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.auth.auth_controller import AuthController
from app.core.database import get_db
from app.schemas.user.user import Token, UserCreate, UserLogin, UserRead

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    return AuthController(db).register(payload)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    return AuthController(db).login(payload)
