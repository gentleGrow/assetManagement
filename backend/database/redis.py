from redis.asyncio import Redis


class RedisRealTimeStockRepository:
    @staticmethod
    async def bulk_get(redis_client: Redis, keys: list[str]) -> list[int]:
        return await redis_client.mget(keys)

    @staticmethod
    async def save(redis_client: Redis, key: str, price: int, expire_time: int) -> None:
        await redis_client.set(key, price, ex=expire_time)


class RedisExchangeRateRepository:
    @staticmethod
    async def bulk_get(redis_client: Redis, keys: list[str]) -> list[float]:
        return await redis_client.mget(keys)

    @staticmethod
    async def save(redis_client: Redis, key: str, data: float, expire_time: int) -> None:
        await redis_client.set(key, data, ex=expire_time)


class RedisDummyAssetRepository:
    @staticmethod
    async def get(redis_client: Redis, key: str) -> str:
        return await redis_client.get(key)

    @staticmethod
    async def save(redis_client: Redis, key: str, data: str, expire_time: int) -> None:
        await redis_client.set(key, data, ex=expire_time)


class RedisSessionRepository:
    @staticmethod
    async def get(redis_client: Redis, key: str) -> str:
        return await redis_client.get(key)

    @staticmethod
    async def save(redis_client: Redis, key: str, data: str, expire_time: int) -> None:
        await redis_client.set(key, data, ex=expire_time)
