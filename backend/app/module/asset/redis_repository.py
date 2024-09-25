from redis.asyncio import Redis


class RedisRealTimeStockRepository:
    @staticmethod
    async def bulk_get(redis_client: Redis, keys: list[str]) -> list[int]:
        return await redis_client.mget(keys)

    @staticmethod
    async def save(redis_client: Redis, key: str, price: int, expire_time: int) -> None:
        await redis_client.set(key, price, ex=expire_time)

    @staticmethod
    async def bulk_save(redis_client: Redis, stock_data: list[tuple[str, int]], expire_time: int) -> None:
        async with redis_client.pipeline() as pipe:
            for key, price in stock_data:
                pipe.set(key, price, ex=expire_time)
            await pipe.execute()


class RedisExchangeRateRepository:
    @staticmethod
    async def bulk_get(redis_client: Redis, keys: list[str]) -> list[float]:
        return await redis_client.mget(keys)

    @staticmethod
    async def save(redis_client: Redis, key: str, data: float, expire_time: int) -> None:
        await redis_client.set(key, data, ex=expire_time)


class RedisRealTimeMarketIndexRepository:
    @staticmethod
    async def bulk_save(redis_client: Redis, bulk_data: list, expire_time: int) -> None:
        pipeline = redis_client.pipeline()
        for key, market_index_json in bulk_data:
            pipeline.set(key, market_index_json, ex=expire_time)
        await pipeline.execute()
