import hashlib
from datetime import timezone, datetime, timedelta

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.core.config import settings
from backend.core.exeptions import ExpiredToken, InvalidToken, NoRefreshToken
from backend.logger.logger import logger
from backend.models.settings import RefreshTokenModel

from backend.models.users import User_Type

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def create_access_token(user_id: int):
    expired_at = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"user_id": user_id,
               "exp": expired_at.timestamp(),
               "role": User_Type.USER.value}
    access_token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
    return access_token


def verify_access_token(access_token: str):
    try:
        decoded = jwt.decode(access_token, key=settings.SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Signature has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def hash_refresh_token(refresh_token: str) -> str:
    return hashlib.sha256(refresh_token.encode()).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_refresh_token(user_id: int):
    expired_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"user_id": user_id,
               "exp": expired_at.timestamp(),
               "role": User_Type.USER.value}
    refresh_token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
    return refresh_token


def verify_refresh_token(refresh_token: str):
    try:
        decoded = jwt.decode(refresh_token, key=settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ExpiredToken("Token expired")
    except jwt.InvalidTokenError:
        raise InvalidToken("Invalid token")
    return decoded


async def search_refresh_token(user_token: str, user_id: int, db: AsyncSession):
    hash_refresh = hash_refresh_token(user_token)
    result = await db.execute(
        select(RefreshTokenModel).where(RefreshTokenModel.user_id == user_id,
                                        RefreshTokenModel.token_hash == hash_refresh)
    )
    tokens = result.scalars().first()
    if not tokens:
        raise NoRefreshToken()

    return create_access_token(user_id)


async def remove_expired_tokens(db: AsyncSession, user_id: int | None = None):
    try:
        query = delete(RefreshTokenModel).where(RefreshTokenModel.expired_at < datetime.now(timezone.utc))
        if user_id is not None:
            query = query.where(RefreshTokenModel.user_id == user_id)

        await db.execute(query)
        await db.commit()
        logger.info(
            f"Expired tokens removed for user_id={user_id}" if user_id else "Expired tokens removed for all users")
    except Exception as e:
        logger.error(f"Failed to remove expired tokens: {e}")
