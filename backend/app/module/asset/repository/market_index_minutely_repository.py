from sqlalchemy import extract, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.model import MarketIndexMinutely


class MarketIndexMinutelyRepository:
    @staticmethod
    async def get_by_range(session: AsyncSession, date_range: tuple, name: str) -> list[MarketIndexMinutely]:
        start_date, end_date = date_range
        stmt = select(MarketIndexMinutely).where(
            MarketIndexMinutely.datetime.between(start_date, end_date), MarketIndexMinutely.name == name
        )

        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_by_range_interval_minute(
        session: AsyncSession,
        date_range: tuple,
        name: str,
        interval: int,
    ) -> list[MarketIndexMinutely]:
        start_date, end_date = date_range

        stmt = select(MarketIndexMinutely).where(
            MarketIndexMinutely.datetime.between(start_date, end_date),
            MarketIndexMinutely.name == name,
            (extract("minute", MarketIndexMinutely.datetime) % interval == 0),
        )

        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def bulk_upsert(session: AsyncSession, market_indexes: list[MarketIndexMinutely]) -> None:
        stmt = insert(MarketIndexMinutely).values(
            [
                {
                    "name": market_index.name,
                    "datetime": market_index.datetime,
                    "current_price": market_index.current_price,
                }
                for market_index in market_indexes
            ]
        )

        update_dict = {"current_price": stmt.inserted.current_price}

        upsert_stmt = stmt.on_duplicate_key_update(update_dict)

        try:
            await session.execute(upsert_stmt)
            await session.commit()
        except Exception:
            await session.rollback()
