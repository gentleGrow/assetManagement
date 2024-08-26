import asyncio

import yfinance
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.common.service import get_all_stock_code_list
from app.data.yahoo.source.service import format_stock_code
from app.module.asset.enum import Country, MarketIndex
from app.module.asset.model import Stock  # noqa: F401 > relationship 설정시 필요합니다.
from app.module.asset.model import Dividend
from app.module.asset.repository.dividend_repository import DividendRepository
from app.module.asset.schema.stock_schema import StockInfo
from app.module.auth.model import User  # noqa: F401 > relationship 설정시 필요합니다.
from database.dependency import get_mysql_session


async def insert_dividend_data(session: AsyncSession, stock_list: list[StockInfo]):
    dividend_list = []
    for stock in stock_list:
        try:
            country_enum = Country[stock.country.upper()]
            market_index_enum = MarketIndex[stock.market_index.upper()]

            stock_code = format_stock_code(stock.code, country_enum, market_index_enum)
            stock_info = yfinance.Ticker(stock_code)

        except Exception as e:
            print(f"[분석][insert_dividend_data] Error during dividend processing: {e}")
            continue

        dividends = stock_info.dividends

        if dividends is None or dividends.empty:
            newest_dividend = 0
        else:
            newest_dividend = dividends.iloc[-1]

        dividend = Dividend(dividend=newest_dividend, stock_code=stock.code)
        dividend_list.append(dividend)

    try:
        await DividendRepository.bulk_upsert(session=session, dividends=dividend_list)
    except Exception:
        await session.rollback()


async def main():
    print("배당금 수집을 시작합니다.")
    stock_list: list[StockInfo] = get_all_stock_code_list()

    async with get_mysql_session() as session:
        await insert_dividend_data(session, stock_list)

        print("배당금 수집을 완료합니다.")


if __name__ == "__main__":
    asyncio.run(main())
