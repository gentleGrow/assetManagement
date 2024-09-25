import asyncio

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.util.time import get_now_datetime
from app.data.common.constant import STOCK_CACHE_SECOND, STOCK_CHUNK_SIZE
from app.data.common.service import StockCodeFileReader
from app.data.naver.sources.service import get_stock_prices
from app.module.asset.model import StockMinutely
from app.module.asset.redis_repository import RedisRealTimeStockRepository
from app.module.asset.repository.stock_minutely_repository import StockMinutelyRepository
from app.module.asset.schema import StockInfo
from app.module.auth.model import User  # noqa: F401 > relationship 설정시 필요합니다.
from database.dependency import get_mysql_session, get_redis_pool


async def collect_stock_data(redis_client: Redis, session: AsyncSession) -> None:
    stock_code_list: list[StockInfo] = StockCodeFileReader.get_korea_stock_code_list()
    now = get_now_datetime()

    for i in range(0, len(stock_code_list), STOCK_CHUNK_SIZE):
        stock_info_list: list[StockInfo] = stock_code_list[i : i + STOCK_CHUNK_SIZE]
        code_price_pairs: list[tuple[str, int | Exception]] = await get_stock_prices(stock_info_list)

        db_bulk_data = []

        for code, price in code_price_pairs:
            current_stock_data = StockMinutely(code=code, datetime=now, current_price=price)
            db_bulk_data.append(current_stock_data)

            if isinstance(price, Exception):
                continue
            else:
                await RedisRealTimeStockRepository.save(redis_client, code, price, expire_time=STOCK_CACHE_SECOND)

        await StockMinutelyRepository.bulk_upsert(session, db_bulk_data)


async def main():
    redis_client = get_redis_pool()
    async with get_mysql_session() as session:
        while True:
            try:
                await collect_stock_data(redis_client, session)
            except Exception:
                continue
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
