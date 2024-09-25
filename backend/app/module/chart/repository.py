from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from app.module.chart.model import InvestTip


class TipRepository:
    @staticmethod
    async def get(session: AsyncSession, tip_id: int) -> InvestTip:
        result = await session.execute(select(InvestTip).where(InvestTip.id == tip_id))
        return result.scalar_one_or_none()

    staticmethod

    async def save_invest_tips(session: AsyncSession, tips: list[dict]) -> None:
        insert_stmt = insert(InvestTip).values(tips)

        on_duplicate_stmt = insert_stmt.on_duplicate_key_update(tip=insert_stmt.inserted.tip, updated_at=func.now())

        await session.execute(on_duplicate_stmt)
        await session.commit()

    @staticmethod
    async def check(session: AsyncSession, tip_id: int) -> bool:
        result = await session.execute(select(func.count(InvestTip.id)).where(InvestTip.id == tip_id))
        count = result.scalar_one()
        return count > 0
