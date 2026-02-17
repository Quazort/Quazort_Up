from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from sqlalchemy.exc import OperationalError

from core.config import db_config

engine = create_async_engine(db_config.DB)

new_session_factory = async_sessionmaker(engine)

async def get_session():
    async with new_session_factory() as session:
        yield session

