from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserLogin


class AuthController:
    def __init__(self, db: Session):
        self.db = db

    def register(self, payload: UserCreate) -> User:
        email = str(payload.email).lower()
        if self.db.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=409, detail="Email is already registered")
        user = User(
            email=email,
            name=payload.name,
            profile=payload.profile,
            hashed_password=hash_password(payload.password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def login(self, payload: UserLogin) -> Token:
        user = self.db.query(User).filter(User.email == str(payload.email).lower()).first()
        if user is None or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return Token(access_token=create_access_token(str(user.id)))