import asyncio
import logging

import yfinance

from app.data.common.constant import STOCK_CACHE_SECOND
from app.module.asset.constant import CURRENCY_PAIRS
from database.dependency import get_redis_pool
from database.redis import RedisExchangeRateRepository

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


async def fetch_exchange_rate(source_currency: str, target_currency: str) -> float | None:
    url = f"{source_currency}{target_currency}=X"
    try:
        ticker = yfinance.Ticker(url)
        exchange_rate_history = ticker.history(period="1d")
        if not exchange_rate_history.empty:
            rate = exchange_rate_history["Close"].iloc[0]
            return rate
    except Exception:
        return None
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
            logging.error(f"An unexpected error occurred in the main loop: {e}")

        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
