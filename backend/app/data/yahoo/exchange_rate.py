import asyncio

import yfinance
from icecream import ic

from app.data.common.constant import STOCK_CACHE_SECOND
from app.module.asset.constant import CURRENCY_PAIRS
from app.module.asset.redis_repository import RedisExchangeRateRepository
from database.dependency import get_redis_pool


async def fetch_exchange_rate(source_currency: str, target_currency: str) -> float | None:
    url = f"{source_currency}{target_currency}=X"
    try:
        ticker = yfinance.Ticker(url)
        exchange_rate_history = ticker.history(period="1d")

        if exchange_rate_history.empty:
            ic(f"No data found for {url}")
            return None

        rate = exchange_rate_history["Close"].iloc[0]
        return rate
    except Exception as e:
        ic(e)
        return None


async def main():
    redis_client = get_redis_pool()

    while True:
        try:
            for source_currency, target_currency in CURRENCY_PAIRS:
                rate = await fetch_exchange_rate(source_currency, target_currency)

                if rate is None:
                    continue

                cache_key = source_currency + "_" + target_currency
                await RedisExchangeRateRepository.save(redis_client, cache_key, rate, expire_time=STOCK_CACHE_SECOND)
        except Exception as e:
            ic(e)

        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
