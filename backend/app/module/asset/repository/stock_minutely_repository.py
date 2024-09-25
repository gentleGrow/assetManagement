from sqlalchemy import extract, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.model import StockMinutely


class StockMinutelyRepository:
    @staticmethod
    async def get_by_range_interval_minute(
        session: AsyncSession,
        date_range: tuple,
        codes: list[str],
        interval: int,
    ) -> list[StockMinutely]:
        start_date, end_date = date_range

        stmt = select(StockMinutely).where(
            StockMinutely.datetime.between(start_date, end_date),
            StockMinutely.code.in_(codes),
            (extract("minute", StockMinutely.datetime) % interval == 0),
        )

        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def bulk_upsert(session: AsyncSession, stocks: list[StockMinutely]) -> None:
        stmt = insert(StockMinutely).values(
            [
                {
                    "code": stock.code,
                    "datetime": stock.datetime,
                    "current_price": stock.current_price,
                }
                for stock in stocks
            ]
        )

        update_dict = {"current_price": stmt.inserted.current_price}

        upsert_stmt = stmt.on_duplicate_key_update(update_dict)

        try:
            await session.execute(upsert_stmt)
            await session.commit()
        except Exception:
            await session.rollback()
