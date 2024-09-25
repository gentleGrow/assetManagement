from redis.asyncio import Redis

from app.module.asset.constant import CURRENCY_PAIRS
from app.module.asset.enum import CurrencyType
from app.module.asset.model import Asset
from app.module.asset.redis_repository import RedisExchangeRateRepository


class ExchangeRateService:
    @staticmethod
    def get_won_exchange_rate(asset: Asset, exchange_rate_map: dict[str, float]) -> float:
        source_country = asset.asset_stock.stock.country.upper().strip()
        source_currency = CurrencyType[source_country]
        if source_currency == CurrencyType.KOREA:
            return 1.0
        return float(exchange_rate_map.get(f"{source_currency}_{CurrencyType.KOREA}", 0.0))

    @staticmethod
    def get_dollar_exchange_rate(asset: Asset, exchange_rate_map: dict[str, float]) -> float:
        source_country = asset.asset_stock.stock.country.upper().strip()
        source_currency = CurrencyType[source_country]
        if source_currency == CurrencyType.USA:
            return 1.0
        return float(exchange_rate_map.get(f"{source_currency}_{CurrencyType.USA}", 0.0))

    @staticmethod
    async def get_exchange_rate_map(redis_client: Redis) -> dict[str, float]:
        result = {}
        keys = [f"{source_currency}_{target_currency}" for source_currency, target_currency in CURRENCY_PAIRS]
        exchange_rates: list[float] = await RedisExchangeRateRepository.bulk_get(redis_client, keys)

        for i, key in enumerate(keys):
            rate = exchange_rates[i]
            result[key] = float(rate) if rate is not None else 0.0
        return result

    @staticmethod
    def get_exchange_rate(source: CurrencyType, target: CurrencyType, exchange_rate_map: dict[str, float]) -> float:
        if source == target:
            return 1.0
        return float(exchange_rate_map.get(f"{source}_{target}", 0.0))
