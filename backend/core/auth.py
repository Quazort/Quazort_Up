from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.engine import get_session
from backend.logger.logger import logger
from backend.models.users import UsersModel
from backend.services.auth import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(db: AsyncSession = Depends(get_session), access_token: str = Depends(oauth2_scheme)):
    """Функция получает access token, расшифровывает его и отдает его"""

    try:
        verify_token = verify_access_token(access_token)
        query = await db.execute(select(UsersModel).where(UsersModel.id == verify_token["user_id"]))
        user = query.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401,detail="Unauthorized access")
        if user.deleted:
            raise HTTPException(status_code=404,detail="Not found")
        return user
    except HTTPException:
        raise
    except Exception as ex:
        logger.error(f"get_current_user:{ex}")
        raise HTTPException(status_code=500,detail=str(ex))
