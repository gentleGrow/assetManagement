from icecream import ic
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from app.module.asset.model import Dividend


class DividendRepository:
    @staticmethod
    async def get_dividends_recent(session: AsyncSession, stock_codes: list[str]) -> list[Dividend]:
        subquery = (
            select(Dividend.stock_code, func.max(Dividend.date).label("max_date"))
            .where(Dividend.stock_code.in_(stock_codes))
            .group_by(Dividend.stock_code)
            .subquery()
        )

        query = select(Dividend).join(
            subquery, (Dividend.stock_code == subquery.c.stock_code) & (Dividend.date == subquery.c.max_date)
        )

        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_dividend(session: AsyncSession, stock_code: str) -> Dividend:
        result = await session.execute(select(Dividend).where(Dividend.stock_code == stock_code))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_dividends(session: AsyncSession, stock_codes: list[str]) -> list[Dividend]:
        result = await session.execute(select(Dividend).where(Dividend.stock_code.in_(stock_codes)))
        return result.scalars().all()

    @staticmethod
    async def save(session: AsyncSession, dividend: Dividend) -> None:
        session.add(dividend)
        await session.commit()

    @staticmethod
    async def upsert(session: AsyncSession, dividend: Dividend) -> None:
        dividend_value = float(dividend.dividend)
        stock_code_value = str(dividend.stock_code)

        query_statement = insert(Dividend).values(
            dividend=dividend_value,
            stock_code=stock_code_value,
        )

        on_duplicate_stmt = query_statement.on_duplicate_key_update(
            dividend=query_statement.inserted.dividend, updated_at=func.now()
        )

        await session.execute(on_duplicate_stmt)
        await session.commit()

    @staticmethod
    async def bulk_upsert(session: AsyncSession, dividends: list[Dividend]) -> None:
        stmt = insert(Dividend).values(
            [
                {"dividend": float(dividend.dividend), "stock_code": str(dividend.stock_code), "date": dividend.date}
                for dividend in dividends
            ]
        )

        update_stmt = {"dividend": stmt.inserted.dividend, "updated_at": func.now()}

        upsert_stmt = stmt.on_duplicate_key_update(update_stmt)

        try:
            await session.execute(upsert_stmt)
            await session.commit()
            ic("성공적으로 저장하였습니다.")
        except Exception as e:
            await session.rollback()
            ic(f"저장에 실패했습니다. 에러: {e}")
