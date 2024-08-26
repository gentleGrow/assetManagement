from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from app.module.asset.model import Dividend


class DividendRepository:
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
        if not dividends:
            return

        values = [{"dividend": float(div.dividend), "stock_code": str(div.stock_code)} for div in dividends]

        query_statement = insert(Dividend).values(values)
        on_duplicate_stmt = query_statement.on_duplicate_key_update(
            dividend=query_statement.inserted.dividend, updated_at=func.now()
        )

        try:
            await session.execute(on_duplicate_stmt)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise Exception(f"Failed to bulk upsert dividends: {e}")
