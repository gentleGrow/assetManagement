from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.enum import AccountType, AssetType, InvestmentBankType, PurchaseCurrencyType
from app.module.asset.model import Asset
from app.module.asset.repository.asset_repository import AssetRepository
from app.module.asset.schema import AssetStockPutRequest
from app.module.asset.services.asset_service import AssetService


class TestAssetService:
    async def test_get_asset_map_success(
        self,
        session: AsyncSession,
        setup_asset,
    ):
        # Given
        asset_id = 1

        # When
        result = await AssetService.get_asset_map(session, asset_id)

        # Then
        assert result is not None
        assert isinstance(result, dict)
        assert result[asset_id].id == asset_id
        assert result[asset_id].asset_type == AssetType.STOCK
        assert result[asset_id].asset_stock.purchase_price == 500.0

    async def test_update_asset_stock(self, session: AsyncSession, setup_all):
        # Given
        asset_id = 1
        asset: Asset = await AssetRepository.get_asset_by_id(session, asset_id)

        request_data = AssetStockPutRequest(
            id=asset.id,
            buy_date=date(2024, 9, 1),
            purchase_currency_type=PurchaseCurrencyType.KOREA,
            quantity=5,
            stock_code="005930",
            account_type=AccountType.REGULAR,
            investment_bank=InvestmentBankType.KB,
            purchase_price=600.0,
        )

        stock_id = 3

        # When
        await AssetService.save_asset_by_put(session, request_data, asset, stock_id)
        updated_asset = await AssetRepository.get_asset_by_id(session, asset_id)

        # Then
        assert updated_asset.asset_stock.account_type == AccountType.REGULAR
        assert updated_asset.asset_stock.investment_bank == InvestmentBankType.KB
        assert updated_asset.asset_stock.purchase_currency_type == PurchaseCurrencyType.KOREA
        assert updated_asset.asset_stock.purchase_date == date(2024, 9, 1)
        assert updated_asset.asset_stock.purchase_price == 600.0
        assert updated_asset.asset_stock.quantity == 5
        assert updated_asset.asset_stock.stock_id == stock_id
