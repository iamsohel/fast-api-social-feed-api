from typing import List, Union
from datetime import timedelta

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm


from .service import create_user, get_user_by_email, get_users, get_user, get_password_hash, \
    authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user
from .schemas import UserResponse, UserCreate, Token
from app.database.core import get_db

auth_router: APIRouter = APIRouter()
user_router: APIRouter = APIRouter()


@auth_router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hash_password = get_password_hash(user.password)
    user.password = hash_password
    return create_user(db=db, user=user)


@auth_router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.post("/token")
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@user_router.post("/users/", response_model=UserResponse)
def create_users(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@user_router.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_active_user)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@user_router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserResponseUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@user_router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


@user_router.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_active_user)):
    return current_user


@auth_router.get("/users/me/items/")
async def read_own_items(current_user: UserResponse = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.email}]
