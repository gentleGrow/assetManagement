import argparse
import asyncio
import json

import yfinance
from icecream import ic
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.util.time import get_now_datetime
from app.data.common.constant import STOCK_CACHE_SECOND
from app.data.yahoo.source.service import format_stock_code
from app.module.asset.enum import Country
from app.module.asset.model import StockMinutely
from app.module.asset.redis_repository import RedisRealTimeStockRepository
from app.module.asset.repository.stock_minutely_repository import StockMinutelyRepository
from app.module.asset.schema import StockInfo
from database.dependency import get_mysql_session, get_redis_pool


def fetch_stock_price(stock_code: str, code: str) -> tuple[str, float]:
    try:
        stock = yfinance.Ticker(stock_code)
        current_price = stock.info.get("bid")
        return code, current_price
    except ValueError as ve:
        ic(f"Error fetching stock data for {stock_code}: {ve}")
        return code, 0.0
    except Exception as e:
        ic(f"Error fetching stock data: {e}")
        return code, 0.0


async def collect_stock_data(redis_client: Redis, session: AsyncSession, stock_code_list: list[StockInfo]) -> None:
    now = get_now_datetime()
    code_price_pairs = []
    db_bulk_data = []
    fetch_tasks = []

    event_loop = asyncio.get_event_loop()

    for stock_dict in stock_code_list:
        trimmed_stock_dict = {
            key: value.strip() if isinstance(value, str) else value for key, value in stock_dict.items()
        }
        stockinfo = StockInfo(**trimmed_stock_dict)
        try:
            country = Country[stockinfo.country.upper().replace(" ", "_")]
            stock_code = format_stock_code(
                stockinfo.code,
                country,
                stockinfo.market_index.upper(),
            )

            fetch_tasks.append(event_loop.run_in_executor(None, fetch_stock_price, stock_code, stockinfo.code))
        except Exception as e:
            ic(f"Error formatting stock code: {e}")
            continue

    code_price_pairs = await asyncio.gather(*fetch_tasks)

    redis_bulk_data = [(code, price) for code, price in code_price_pairs if price]

    for code, price in redis_bulk_data:
        current_stock_data = StockMinutely(code=code, datetime=now, current_price=price)
        db_bulk_data.append(current_stock_data)

    if redis_bulk_data:
        await RedisRealTimeStockRepository.bulk_save(redis_client, redis_bulk_data, expire_time=STOCK_CACHE_SECOND)

    if db_bulk_data:
        await StockMinutelyRepository.bulk_upsert(session, db_bulk_data)


async def main():
    parser = argparse.ArgumentParser(description="Process stock code chunk.")
    parser.add_argument("stock_code_list", type=str, help="JSON serialized list of stock codes")
    args = parser.parse_args()

    stock_code_list_chunk = json.loads(args.stock_code_list)
    redis_client = get_redis_pool()

    while True:
        try:
            async with get_mysql_session() as session:
                await collect_stock_data(redis_client, session, stock_code_list_chunk)
        except Exception as e:
            ic(f"Error occurred: {e}")
        finally:
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
