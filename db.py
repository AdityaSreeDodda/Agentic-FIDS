import logging

import asyncpg

from config import settings

logger = logging.getLogger(__name__)


class DB:
    pool: asyncpg.Pool | None = None


db = DB()


async def connect_db() -> None:
    db.pool = await asyncpg.create_pool(settings.DATABASE_URL)
    logger.info("Database connection pool created")


async def close_db() -> None:
    if db.pool:
        await db.pool.close()
        logger.info("Database connection pool closed")