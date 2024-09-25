from datetime import date

from sqlalchemy import func, tuple_
from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased

from app.module.asset.model import StockDaily


class StockDailyRepository:
    @staticmethod
    async def get_stock_dailies_by_code_and_date(
        session: AsyncSession, stock_code_date_pairs: list[tuple[str, date]]
    ) -> list[StockDaily]:
        stmt = select(StockDaily).where(tuple_(StockDaily.code, StockDaily.date).in_(stock_code_date_pairs))
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_latest(session: AsyncSession, stock_codes: list[str]) -> list[StockDaily]:
        subquery = (
            select(StockDaily.code, func.max(StockDaily.date).label("max_date"))
            .where(StockDaily.code.in_(stock_codes))
            .group_by(StockDaily.code)
            .subquery()
        )

        stock_daily_alias = aliased(StockDaily)

        stmt = select(stock_daily_alias).join(
            subquery, (stock_daily_alias.code == subquery.c.code) & (stock_daily_alias.date == subquery.c.max_date)
        )

        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_stock_daily(session: AsyncSession, stock_code: str, stock_date: date) -> StockDaily:
        result = await session.execute(
            select(StockDaily).where(StockDaily.code == stock_code, StockDaily.date == stock_date)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_stock_dailies(session: AsyncSession, stock_codes: list[str]) -> list[StockDaily]:
        result = await session.execute(select(StockDaily).where(StockDaily.code.in_(stock_codes)))
        return result.scalars().all()

    @staticmethod
    async def get_most_recent_stock_daily(session: AsyncSession, stock_code: str) -> StockDaily:
        result = await session.execute(
            select(StockDaily).where(StockDaily.code == stock_code).order_by(StockDaily.date.desc()).limit(1)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_most_recent_stock_dailies(session: AsyncSession, stock_codes: list[str]) -> list[StockDaily]:
        subquery = (
            session.query(StockDaily.code, func.max(StockDaily.date).label("max_date"))
            .where(StockDaily.code.in_(stock_codes))
            .group_by(StockDaily.code)
            .subquery()
        )

        result = await session.execute(
            select(StockDaily)
            .join(subquery, (StockDaily.code == subquery.c.code) & (StockDaily.date == subquery.c.max_date))
            .where(StockDaily.code.in_(stock_codes))
        )

        return result.scalars().all()

    @staticmethod
    async def bulk_upsert(session: AsyncSession, stock_dailies: list[StockDaily]) -> None:
        stmt = mysql_insert(StockDaily).values(
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
        except Exception:
            await session.rollback()
