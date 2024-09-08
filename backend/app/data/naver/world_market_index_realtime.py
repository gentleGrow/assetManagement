import asyncio
from datetime import datetime

from redis.asyncio import Redis
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.common.constant import MARKET_INDEX_CACHE_SECOND
from app.module.asset.constant import COUNTRY_TRANSLATIONS, INDEX_NAME_TRANSLATIONS
from app.module.asset.enum import MarketIndex
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
    now = datetime.now().replace(second=0, microsecond=0)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://finance.naver.com/world/")
        redis_bulk_data = []
        db_bulk_data = []

        america_index_table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "americaIndex")))

        tr_rows = america_index_table.find_elements(By.XPATH, ".//thead/tr")

        for tr_row in tr_rows:
            tr_row_data = []
            tds = tr_row.find_elements(By.TAG_NAME, "td")

            for td in tds:
                if "graph" in td.get_attribute("class"):
                    continue

                span = td.find_elements(By.TAG_NAME, "span")
                if span:
                    tr_row_data.append(span[0].text)
                else:
                    a_elements = td.find_elements(By.TAG_NAME, "a")
                    if a_elements:
                        tr_row_data.append(a_elements[0].text)
                    else:
                        tr_row_data.append(td.text)

            if tr_row_data:
                country_kr = tr_row_data[0]
                if country_kr in COUNTRY_TRANSLATIONS:
                    country_en = COUNTRY_TRANSLATIONS[country_kr]
                else:
                    continue
                index_name_kr = tr_row_data[1]
                index_name_en = INDEX_NAME_TRANSLATIONS.get(index_name_kr, index_name_kr)

                current_value = tr_row_data[2].strip().replace(",", "")
                change_value = tr_row_data[3].strip().replace(",", "")
                change_percent = tr_row_data[4].strip().replace("%", "")
                change_percent = change_percent

                market_index = MarketIndexData(
                    country=country_en,
                    index_name=index_name_en,
                    current_value=current_value,
                    change_value=change_value,
                    change_percent=change_percent,
                    update_time=tr_row_data[5],
                )

                current_index = MarketIndexMinutely(index_name=index_name_en, datetime=now, current_price=current_value)

                db_bulk_data.append(current_index)

                if market_index:
                    market_index_json = market_index.model_dump_json()
                    redis_bulk_data.append((index_name_en, market_index_json))

        await MarketIndexMinutelyRepository.bulk_upsert(session, db_bulk_data)
        await RedisRealTimeMarketIndexRepository.bulk_save(
            redis_client, redis_bulk_data, expire_time=MARKET_INDEX_CACHE_SECOND
        )

    finally:
        driver.quit()


async def main():
    redis_client = await get_redis_pool()
    async with get_mysql_session() as session:
        while True:
            await fetch_market_data(redis_client, session)
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())