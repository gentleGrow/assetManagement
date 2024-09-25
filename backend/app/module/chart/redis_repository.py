from redis.asyncio import Redis


class RedisRichPortfolioRepository:
    @staticmethod
    async def gets(redis_client: Redis, keys: list[str]) -> list[str]:
        rich_portfolios = await redis_client.mget(*keys)
        return [rich_portfolio if rich_portfolio is not None else None for rich_portfolio in rich_portfolios]

    @staticmethod
    async def get(redis_client: Redis, key: str) -> str:
        return await redis_client.get(key)

    @staticmethod
    async def save(redis_client: Redis, key: str, data: str, expire_time: int) -> None:
        await redis_client.set(key, data, ex=expire_time)


class RedisRichPickRepository:
    @staticmethod
    async def get(redis_client: Redis, key: str) -> str:
        return await redis_client.get(key)

    @staticmethod
    async def save(redis_client: Redis, key: str, data: str, expire_time: int) -> None:
        await redis_client.set(key, data, ex=expire_time)


class RedisTipRepository:
    @staticmethod
    async def get(redis_client: Redis, key: str) -> str:
        return await redis_client.get(key)

    @staticmethod
    async def save(redis_client: Redis, key: str, data: int, expire_time: int) -> None:
        await redis_client.set(key, data, ex=expire_time)


class RedisMarketIndiceRepository:
    @staticmethod
    async def get(redis_client: Redis, key: str) -> str | None:
        return await redis_client.get(key)

    @staticmethod
    async def gets(redis_client: Redis, keys: list[str]) -> list[str]:
        market_index_values = await redis_client.mget(*keys)
        return [
            market_index_value if market_index_value is not None else None for market_index_value in market_index_values
        ]

    @staticmethod
    async def save(redis_client: Redis, key: str, market_index_value: str, expire_time: int) -> None:
        await redis_client.set(key, market_index_value, ex=expire_time)
