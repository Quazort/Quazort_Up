import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from backend.core.config import settings
from backend.logger.logger import logger

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
        await engine.dispose()
        async with asyncio.timeout(5):
            async with engine.connect() as conn:
                await conn.execute(text("select 1"))
    except Exception as e:
        logger.error(f"database error: {e}")


