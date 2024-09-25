import asyncio

import requests
from bs4 import BeautifulSoup
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.util.time import get_now_datetime
from app.data.common.constant import MARKET_INDEX_CACHE_SECOND
from app.module.asset.enum import Country, MarketIndex
from app.module.asset.model import (  # noqa: F401 > relationship 설정시 필요합니다.
    MarketIndexMinutely,
    Stock,
    StockDaily,
    StockMonthly,
    StockWeekly,
)
from app.module.asset.redis_repository import RedisRealTimeMarketIndexRepository
from app.module.asset.repository.market_index_minutely_repository import MarketIndexMinutelyRepository
from app.module.asset.schema import MarketIndexData
from app.module.auth.model import User  # noqa: F401 > relationship 설정시 필요합니다.
from database.dependency import get_mysql_session, get_redis_pool


async def fetch_market_data(redis_client: Redis, session: AsyncSession):
    url = "https://finance.naver.com/"
    now = get_now_datetime()
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    redis_bulk_data = []
    db_bulk_data = []

    section_stock_market = soup.find("div", {"class": "section_stock_market"})

    kospi_area = soup.find("div", {"class": "kospi_area"})
    kospi_current_value = kospi_area.find("span", {"class": "num"}).text.strip().replace(",", "")
    kospi_change_value = kospi_area.find("span", {"class": "num2"}).text.strip().replace(",", "")
    num3_span = kospi_area.find("span", {"class": "num3"})
    percent_change = (
        num3_span.text.replace(num3_span.find("span", {"class": "blind"}).text, "").strip().replace("%", "")
    )

    kospi_db = MarketIndexMinutely(name=MarketIndex.KOSPI, datetime=now, current_price=kospi_current_value)

    db_bulk_data.append(kospi_db)

    kospi_index = MarketIndexData(
        country=Country.KOREA,
        name=MarketIndex.KOSPI,
        current_value=kospi_current_value,
        change_value=kospi_change_value,
        change_percent=percent_change,
        update_time="",
    )

    kospi_index_json = kospi_index.model_dump_json()

    redis_bulk_data.append((MarketIndex.KOSPI, kospi_index_json))

    kosdaq_area = section_stock_market.find("div", {"class": "kosdaq_area"})
    kosdaq_current_value = kosdaq_area.find("span", {"class": "num"}).text.strip().replace(",", "")
    kosdaq_change_value = kosdaq_area.find("span", {"class": "num2"}).text.strip().replace(",", "")
    num3_span = kosdaq_area.find("span", {"class": "num3"})
    percent_change = "".join(num3_span.stripped_strings).replace("%", "").strip()

    kosdaq_db = MarketIndexMinutely(name=MarketIndex.KOSDAQ, datetime=now, current_price=kosdaq_current_value)

    db_bulk_data.append(kosdaq_db)

    kosdaq_index = MarketIndexData(
        country=Country.KOREA,
        name=MarketIndex.KOSDAQ,
        current_value=kosdaq_current_value,
        change_value=kosdaq_change_value,
        change_percent=percent_change,
        update_time="",
    )

    kosdaq_index_json = kosdaq_index.model_dump_json()
    redis_bulk_data.append((MarketIndex.KOSDAQ, kosdaq_index_json))

    await MarketIndexMinutelyRepository.bulk_upsert(session, db_bulk_data)
    await RedisRealTimeMarketIndexRepository.bulk_save(
        redis_client, redis_bulk_data, expire_time=MARKET_INDEX_CACHE_SECOND
    )


async def main():
    redis_client = await get_redis_pool()
    async with get_mysql_session() as session:
        while True:
            await fetch_market_data(redis_client, session)
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
