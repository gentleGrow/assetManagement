import asyncio

import pandas as pd
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.common.service import get_all_stock_code_list
from app.data.yahoo.source.constant import TIME_INTERVAL_MODEL_REPO_MAP, TIME_INTERVAL_REPOSITORY_MAP
from app.data.yahoo.source.schema import StockDataFrame
from app.data.yahoo.source.service import format_stock_code, get_last_week_period_bounds
from app.module.asset.enum import Country, MarketIndex, TimeInterval
from app.module.asset.model import Stock, StockDaily, StockMonthly, StockWeekly  # noqa: F401 > relationship 설정시 필요합니다.
from app.module.asset.schema.stock_schema import StockInfo
from app.module.auth.model import User  # noqa: F401 > relationship 설정시 필요합니다.
from database.dependency import get_mysql_session


async def process_stock_data(session: AsyncSession, stock_list: list[StockInfo], start_period: int, end_period: int):
    for stock_info in stock_list:
        for interval in TimeInterval:
            stock_model = TIME_INTERVAL_MODEL_REPO_MAP[interval]
            interval_repository = TIME_INTERVAL_REPOSITORY_MAP[interval]

            try:
                stock_code = format_stock_code(
                    stock_info.code,
                    Country[stock_info.country.upper().replace(" ", "_")],
                    MarketIndex[stock_info.market_index.upper()],
                )
            except KeyError:
                print(f"Skipping stock with invalid market index: {stock_info.market_index}")
                continue

            url = (
                f"https://query1.finance.yahoo.com/v7/finance/download/{stock_code}"
                f"?period1={start_period}&period2={end_period}&interval={interval.value}"
                f"&events=history&includeAdjustedClose=true"
            )

            try:
                df = pd.read_csv(url)
            except Exception:
                continue

            stock_rows = []

            for _, row in df.iterrows():
                try:
                    stock_dataframe = StockDataFrame(
                        date=row["Date"],
                        open=row["Open"],
                        high=row["High"],
                        low=row["Low"],
                        close=row["Close"],
                        adj_close=row["Adj Close"],
                        volume=row["Volume"],
                    )
                except Exception:
                    continue

                stock_row = stock_model(
                    code=stock_info.code,
                    date=stock_dataframe.date,
                    opening_price=stock_dataframe.open,
                    highest_price=stock_dataframe.high,
                    lowest_price=stock_dataframe.low,
                    close_price=stock_dataframe.close,
                    adj_close_price=stock_dataframe.adj_close,
                    trade_volume=stock_dataframe.volume,
                )

                stock_rows.append(stock_row)

            try:
                await interval_repository.bulk_upsert(session, stock_rows)
            except IntegrityError as e:
                print(f"{e=}")
                await session.rollback()
                continue


async def main():
    start_period, end_period = get_last_week_period_bounds()
    stock_list: list[StockInfo] = get_all_stock_code_list()

    async with get_mysql_session() as session:
        await process_stock_data(session, stock_list, start_period, end_period)


if __name__ == "__main__":
    asyncio.run(main())
