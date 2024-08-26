from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.model import StockMonthly


class StockMonthlyRepository:
    @staticmethod
    async def bulk_upsert(session: AsyncSession, stock_dailies: list[StockMonthly]) -> None:
        stmt = mysql_insert(StockMonthly).values(
            [
                {
                    "code": stock_daily.code,
                    "date": stock_daily.date,
                    "opening_price": stock_daily.opening_price,
                    "highest_price": stock_daily.highest_price,
                    "lowest_price": stock_daily.lowest_price,
                    "close_price": stock_daily.close_price,
                    "adj_close_price": stock_daily.adj_close_price,
                    "trade_volume": stock_daily.trade_volume,
                }
                for stock_daily in stock_dailies
            ]
        )

        update_dict = {
            "opening_price": stmt.inserted.opening_price,
            "highest_price": stmt.inserted.highest_price,
            "lowest_price": stmt.inserted.lowest_price,
            "close_price": stmt.inserted.close_price,
            "adj_close_price": stmt.inserted.adj_close_price,
            "trade_volume": stmt.inserted.trade_volume,
        }

        upsert_stmt = stmt.on_duplicate_key_update(update_dict)

        try:
            await session.execute(upsert_stmt)
            await session.commit()
        except Exception as e:
            print(f"Error during bulk upsert: {e}")
            await session.rollback()
