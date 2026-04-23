import asyncio

import redis.asyncio as redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from backend.core.config import settings
from backend.logger.logger import logger

redis_db = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

engine = create_async_engine(settings.DATABASE_URL,
                             max_overflow=10,
                             pool_size=10,
                             pool_pre_ping=True)

new_session_maker = async_sessionmaker(engine)


async def get_session():
    async with new_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"get_session: {e}")
            raise


async def check_db():
    try:
        async with asyncio.timeout(5):
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
                logger.info("Database connection successful!")
    except Exception as e:
        logger.error(f"database error: {e}")
