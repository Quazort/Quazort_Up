from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from backend.controllers.users import create_user, login_user, check_refresh_token
from backend.db.engine import get_session
from backend.schemas.users import UserCreate, RefreshTokenSchema

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/auth/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_session)):
    user_secret = await create_user(db, user)
    return user_secret


@auth_router.post("/auth/login")
async def login(user: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user_secret = await login_user(user, db)
    return user_secret


@auth_router.post("/auth/refresh")
async def refresh(token: RefreshTokenSchema, db: AsyncSession = Depends(get_session)):
    access_token = await check_refresh_token(token.refresh_token, db)
    return access_token

# TODO Доделать забыл пароль по почте
# @auth_router.post("/auth/forgot_pwd")
# async def change_password():
#     pass