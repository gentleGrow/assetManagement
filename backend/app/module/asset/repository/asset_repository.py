from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound

from app.module.asset.enum import AssetType
from app.module.asset.model import Asset, AssetStock


class AssetRepository:
    @staticmethod
    async def delete_asset(session: AsyncSession, asset_id: int) -> None:
        try:
            asset = await session.execute(
                select(Asset).filter(Asset.id == asset_id).options(joinedload(Asset.asset_stock))
            )
            asset = asset.scalars().one()
        except NoResultFound:
            raise ValueError(f"Asset ID {asset_id}를 찾을 수 없습니다.")

        if asset.asset_stock:
            asset.asset_stock.deleted_at = datetime.now()

        asset.deleted_at = datetime.now()
        await session.commit()

    @staticmethod
    async def get_assets(session: AsyncSession, user_id: str) -> list[Asset]:
        result = await session.execute(select(Asset).filter(and_(Asset.user_id == user_id, Asset.deleted_at is None)))
        return result.scalars().all()

    @staticmethod
    async def save_assets(session: AsyncSession, assets: list[Asset]) -> None:
        session.add_all(assets)
        await session.commit()

    @staticmethod
    async def get_eager(session: AsyncSession, user_id: int, asset_type: AssetType) -> list[Asset]:
        result = await session.execute(
            select(Asset)
            .filter(and_(Asset.user_id == user_id, Asset.asset_type == asset_type, Asset.deleted_at is None))
            .options(joinedload(Asset.asset_stock).joinedload(AssetStock.stock))
        )
        return result.unique().scalars().all()

    @staticmethod
    async def get_assets_by_ids(session: AsyncSession, asset_ids: list[int]) -> list[Asset]:
        result = await session.execute(
            select(Asset)
            .filter(and_(Asset.id.in_(asset_ids), Asset.deleted_at is None))
            .options(joinedload(Asset.asset_stock).joinedload(AssetStock.stock))
        )
        return result.scalars().all()
