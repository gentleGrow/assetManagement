from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.enum import AssetType
from app.module.asset.repository.asset_repository import AssetRepository
from app.module.auth.constant import DUMMY_USER_ID


class TestAssetRepository:
    async def test_get_eager(self, session: AsyncSession, setup_asset):
        # Given
        setup_asset

        # When
        assets = await AssetRepository.get_eager(session, user_id=DUMMY_USER_ID, asset_type=AssetType.STOCK)

        # Then
        asset_1, asset_2 = assets[0], assets[1]

        assert asset_1.user_id == DUMMY_USER_ID
        assert asset_1.asset_type == AssetType.STOCK
        assert asset_1.asset_stock.stock_id == 1
        assert asset_1.asset_stock.purchase_price == 500.0
        assert asset_1.asset_stock.quantity == 1

        assert asset_2.user_id == DUMMY_USER_ID
        assert asset_2.asset_type == AssetType.STOCK
        assert asset_2.asset_stock.stock_id == 2
        assert asset_2.asset_stock.purchase_price == 1000.0
        assert asset_2.asset_stock.quantity == 2
