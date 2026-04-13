from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exeptions import RockError
from backend.logger.logger import logger
from backend.services.rock import get_all_muscles_rock


async def rock_muscles(db: AsyncSession, muscle_id: int):
    try:
        response = await get_all_muscles_rock(db, muscle_id)
        return response
    except RockError:
        logger.warning(f"Not found {muscle_id} or exercises")
        raise HTTPException(status_code=404, detail="Not found")

