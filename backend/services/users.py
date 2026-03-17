from typing import Optional

from pydantic import EmailStr
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from backend.core.exeptions import DataBaseError, UniquenessError
from backend.logger.logger import logger
from backend.models.settings import RefreshTokenModel
from backend.models.users import UsersModel
from backend.services.auth import hash_password, create_access_token, create_refresh_token, hash_refresh_token


async def check_user(username: str, db: AsyncSession, email: Optional[EmailStr] = None) -> Optional[UsersModel] | None:
    """Проверяет пользователя по username и, опционально, по email"""
    try:
        conditions = [UsersModel.username == username]
        if email:
            conditions.append(UsersModel.email == email)

        query = select(UsersModel).where(or_(*conditions))
        result = await db.execute(query)
        return result.scalar_one_or_none()
    except Exception as e:
        logger.exception(f"check_user: {e}")
        raise


async def create_new_user(user_name: str, password: str, email, db: AsyncSession):
    """Функция получает user_name, password, db и создает его в db, возвращает access и refresh токен"""

    try:
        hashed_password = hash_password(password)
        new_user = UsersModel(username=user_name, password_hashed=hashed_password, email=email)
        db.add(new_user)
        await db.flush()
        access_token = create_access_token(new_user.id)
        refresh_token = create_refresh_token(new_user.id)
        hashed_refresh = hash_refresh_token(refresh_token)
        new_refresh_token = RefreshTokenModel(user_id=new_user.id, token_hash=hashed_refresh)

        db.add(new_refresh_token)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }
    except IntegrityError as e:
        logger.error(f"create_new_user: {e}")
        raise UniquenessError()
    except SQLAlchemyError as e:
        logger.error(f"create_new_user: {e}")
        raise DataBaseError()
    except Exception as e:
        logger.error(f"create_new_user: {e}")
        raise


async def login(user, db: AsyncSession):
    try:
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        new_token = RefreshTokenModel(user_id=user.id, token_hash=hash_refresh_token(refresh_token))
        db.add(new_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }
    except Exception as e:
        logger.error(f"login: {e}")
        raise
