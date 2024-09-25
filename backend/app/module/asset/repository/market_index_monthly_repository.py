from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.model import MarketIndexMonthly


class MarketIndexMonthlyRepository:
    @staticmethod
    async def save_market_indexes(session: AsyncSession, market_indexes: list[MarketIndexMonthly]) -> None:
        session.add_all(market_indexes)
        await session.commit()

    @staticmethod
    async def bulk_upsert(session: AsyncSession, market_indexes: list[MarketIndexMonthly]) -> None:
        stmt = insert(MarketIndexMonthly).values(
            [
                {
                    "name": market_index.name,
                    "date": market_index.date,
                    "open_price": market_index.open_price,
                    "high_price": market_index.high_price,
                    "low_price": market_index.low_price,
                    "close_price": market_index.close_price,
                    "volume": market_index.volume,
                }
                for market_index in market_indexes
            ]
        )

        update_dict = {
            "open_price": stmt.inserted.open_price,
            "high_price": stmt.inserted.high_price,
            "low_price": stmt.inserted.low_price,
            "close_price": stmt.inserted.close_price,
            "volume": stmt.inserted.volume,
        }

        upsert_stmt = stmt.on_duplicate_key_update(update_dict)

        try:
            await session.execute(upsert_stmt)
            await session.commit()
        except Exception:
            await session.rollback()
