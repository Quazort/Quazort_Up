import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import db_config

engine = create_async_engine(db_config.DB)

new_session_factory = async_sessionmaker(engine)


async def get_session():
    async with new_session_factory() as session:
        yield session


async def check_db():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            print("Database connected")
    except Exception as e:
        print("Database Error:", e)

