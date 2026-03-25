from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exeptions import ExpiredToken, InvalidToken, NoRefreshToken, DataBaseError, UniquenessError, \
    UserNotFound
from backend.logger.logger import logger
from backend.models.users import UsersModel
from backend.schemas.users import UserCreate
from backend.services.auth import verify_password, verify_refresh_token, search_refresh_token, remove_expired_tokens
from backend.services.users import check_user, create_new_user, login, delete


async def login_user(user, db):
    """Функция авторизует пользователя"""
    try:
        db_user = await check_user(user.username, db)
        if not db_user or not verify_password(user.password, db_user.password_hashed):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        authorization_user = await login(db_user, db)
        return authorization_user
    except HTTPException as e:
        logger.error(f"login_user: {e}")
        raise
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(f"login_user: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error")


async def create_user(db: AsyncSession, user: UserCreate):
    """Тут у нас должна быть регистрация, проверка юзера, потом создание"""

    try:
        check_old_user = await check_user(user.username, db, user.email)
        if check_old_user:
            raise HTTPException(status_code=409, detail="User already exists")

        user_secret = await create_new_user(user.username, user.password, user.email, db)
        return user_secret
    except HTTPException:
        raise
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")
    except DataBaseError:
        raise HTTPException(status_code=500, detail="Unexpected error")
    except UniquenessError:
        raise HTTPException(status_code=409, detail="User already exists")
    except Exception as e:
        logger.error(f"create_user: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error")


async def check_refresh_token(token: str, db: AsyncSession):
    try:
        check_token = verify_refresh_token(token)
        if not check_token:
            raise InvalidToken()

        access_token = await search_refresh_token(token, check_token["user_id"], db)
        return {"access_token": access_token}
    except ExpiredToken:
        await remove_expired_tokens(db)
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except InvalidToken:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    except NoRefreshToken:
        raise HTTPException(status_code=401, detail="No refresh token")
    except Exception as e:
        logger.error(f"check_refresh_token: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error")


async def delete_me(db: AsyncSession, user: UsersModel, password: str):
    try:
        verify_pwd = verify_password(password, user.password_hashed)
        if not verify_pwd:
            raise HTTPException(status_code=401, detail="Invalid password")
        else:
            await delete(user, db)
            return {"detail": "True"}
    except HTTPException:
        raise
    except DataBaseError:
        raise HTTPException(status_code=500, detail="Unexpected error")
    except Exception as e:
        logger.error(f"delete_me: {e}")