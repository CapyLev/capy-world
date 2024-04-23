from contextlib import asynccontextmanager
from typing import AsyncGenerator

from redis.asyncio import client, from_url
from sanic.log import logger

from .constants import constants


class RedisClient:
    _redis: client.Redis | None = None

    async def _connect(self) -> None:
        self._redis = await from_url(
            url=constants.redis.REDIS_URL,
            single_connection_client=constants.redis.REDIS_SINGLE_CONNECTION_CLIENT,
            auto_close_connection_pool=constants.redis.AUTO_CLOSE_CONNECTION_POOL_CLIENT,
        )

    async def _close_connection(self):
        if self._redis:
            await self._redis.aclose()

    @asynccontextmanager
    async def get_redis(self) -> AsyncGenerator[client.Redis, None]:
        if not self._redis:
            await self._connect()

        try:
            yield self._redis
        except Exception as exc:
            logger.error(f"Redis error: {str(exc)}")
        finally:
            await self._close_connection()
