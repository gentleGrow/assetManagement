from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.module.asset.model import AssetField


class AssetFieldRepository:
    @staticmethod
    async def get(session: AsyncSession, user_id: int) -> AssetField | None:
        select_instance = select(AssetField).where(AssetField.user_id == user_id)
        result = await session.execute(select_instance)
        return result.scalars().first()

    @staticmethod
    async def save(session: AsyncSession, asset_field: AssetField) -> None:
        session.add(asset_field)
        await session.commit()

    @staticmethod
    async def update(session: AsyncSession, asset_field: AssetField) -> None:
        await session.merge(asset_field)
        await session.commit()
