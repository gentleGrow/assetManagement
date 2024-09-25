from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.enum import StockAsset
from app.module.asset.services.asset_field_service import AssetFieldService
from app.module.auth.constant import DUMMY_USER_ID


class TestAssetFieldService:
    async def test_get_asset_field_exists(self, session: AsyncSession, setup_asset_field):
        # Given
        setup_asset_field

        # When
        fields_to_disable = ["stock_volume", "purchase_currency_type", "purchase_price", "purchase_amount"]
        expected_fields = [field.value for field in StockAsset if field.value not in fields_to_disable]
        result = await AssetFieldService.get_asset_field(session, DUMMY_USER_ID)

        # Then
        assert result == expected_fields

    async def test_get_asset_field_create_new(self, session: AsyncSession, setup_user):
        # Given
        new_user_id = 2

        # When
        result = await AssetFieldService.get_asset_field(session, new_user_id)

        # Then
        expected_fields = [field.value for field in StockAsset]
        assert result == expected_fields

        # And
        saved_asset_field = await AssetFieldService.get_asset_field(session, new_user_id)
        assert saved_asset_field is not None
        assert saved_asset_field == expected_fields
