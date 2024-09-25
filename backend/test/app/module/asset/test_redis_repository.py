from redis.asyncio import Redis

from app.module.asset.redis_repository import RedisExchangeRateRepository, RedisRealTimeStockRepository


class TestRedisRealTimeStockRepository:
    async def test_bulk_get(self, redis_client: Redis, setup_realtime_stock_price):
        # Given
        keys, expected_values = setup_realtime_stock_price

        # When
        result = await RedisRealTimeStockRepository.bulk_get(redis_client, keys)

        # Then
        assert result == expected_values


class TestRedisExchangeRateRepository:
    async def test_bulk_get(self, redis_client: Redis, setup_exchange_rate):
        # Given
        keys, expected_values = setup_exchange_rate

        # When
        result = await RedisExchangeRateRepository.bulk_get(redis_client, keys)

        # Then
        assert result == expected_values
