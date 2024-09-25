import asyncio

import pandas as pd
import yfinance
from icecream import ic
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.common.service import get_all_stock_code_list
from app.data.yahoo.source.constant import BATCH_SIZE
from app.data.yahoo.source.service import format_stock_code
from app.module.asset.enum import Country
from app.module.asset.model import Dividend
from app.module.asset.repository.dividend_repository import DividendRepository
from app.module.asset.schema import StockInfo
from app.module.auth.model import User  # noqa: F401 > relationship 설정시 필요합니다.
from database.dependency import get_mysql_session


async def insert_dividend_data(session: AsyncSession, stock_list: list[StockInfo], batch_size: int):
    for i in range(0, len(stock_list), batch_size):
        stock_list_batch = stock_list[i : i + batch_size]

        dividend_list = []
        for stock in stock_list_batch:
            try:

                stock_code = format_stock_code(
                    stock.code.strip(), Country[stock.country.upper().strip()], stock.market_index.upper().strip()
                )

                stock_info = yfinance.Ticker(stock_code)

                dividends = stock_info.dividends

                if dividends.empty:
                    continue

                for dividend_date, dividend_amount in dividends.items():
                    try:
                        dividend = Dividend(
                            dividend=dividend_amount, stock_code=stock.code, date=pd.to_datetime(dividend_date).date()
                        )
                    except Exception as e:
                        ic(f"Error processing dividend for stock {stock.code} on {dividend_date}: {e}")
                        continue

                    dividend_list.append(dividend)

            except Exception as e:
                ic(f"[분석][insert_dividend_data] Error during dividend processing for {stock.code}: {e}")
                continue

        await DividendRepository.bulk_upsert(session=session, dividends=dividend_list)


async def main():
    print("배당금 수집을 시작합니다.")
    stock_list: list[StockInfo] = get_all_stock_code_list()

    async with get_mysql_session() as session:
        await insert_dividend_data(session, stock_list, BATCH_SIZE)

    print("배당금 수집을 완료합니다.")


if __name__ == "__main__":
    asyncio.run(main())
