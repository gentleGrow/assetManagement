from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.module.asset.model import AssetStock


class AssetStockRepository:
    @staticmethod
    async def get_asset_stock(session: AsyncSession, asset_id: int) -> AssetStock:
        result = await session.execute(select(AssetStock).where(AssetStock.asset_id == asset_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_asset_stocks(session: AsyncSession, asset_ids: list[int]) -> list[AssetStock]:
        result = await session.execute(select(AssetStock).where(AssetStock.asset_id.in_(asset_ids)))
        return result.scalars().all()

    @staticmethod
    async def save_asset_stocks(session: AsyncSession, asset_stocks: list[AssetStock]) -> None:
        session.add_all(asset_stocks)
        await session.commit()
