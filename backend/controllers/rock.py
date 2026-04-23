from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exeptions import RockError
from backend.db.engine import redis_db
from backend.logger.logger import logger
from backend.schemas.rock import RockResponseSchema
from backend.services.rock import get_all_muscles_rock


async def rock_muscles(db: AsyncSession, muscle_id: int):
    try:
        redis_cache = await redis_db.get(f"rock_muscles:{muscle_id}")
        if redis_cache is not None:
            redis_response = RockResponseSchema.model_validate_json(redis_cache)
            return redis_response

        else:
            response = await get_all_muscles_rock(db, muscle_id)
            cache_muscle = response.model_dump_json()
            await redis_db.set(f"rock_muscles:{muscle_id}", cache_muscle, ex=60)
            return response
    except RockError:
        logger.warning(f"Not found {muscle_id} or exercises")
        raise HTTPException(status_code=404, detail="Not found")
