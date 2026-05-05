from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import schemas, service
from core.database import get_db  # зависимость для получения сессии БД

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = service.create_user(db=db, user_data=user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/login", response_model=schemas.TokenResponse, status_code=status.HTTP_200_OK)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = service.authenticate_user(db=db, email=login_data.email, password=login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    access_token = service.create_access_token(data={"sub": str(user.id)})
    return schemas.TokenResponse(access_token=access_token, token_type="bearer")
