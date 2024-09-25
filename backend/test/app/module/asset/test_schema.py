import pytest
from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.enum import AssetType
from app.module.asset.model import Asset
from app.module.asset.repository.asset_repository import AssetRepository
from app.module.asset.schema import AssetStockResponse, UpdateAssetFieldRequest
from app.module.asset.services.asset_stock_service import AssetStockService
from app.module.asset.services.dividend_service import DividendService
from app.module.asset.services.exchange_rate_service import ExchangeRateService
from app.module.asset.services.stock_daily_service import StockDailyService
from app.module.asset.services.stock_service import StockService
from app.module.auth.constant import DUMMY_USER_ID


class TestUpdateAssetFieldRequest:
    def test_validate_request_data_missing_required_fields(self):
        # Given
        request_data = UpdateAssetFieldRequest(root=["stock_name", "quantity"])

        # When
        try:
            UpdateAssetFieldRequest.validate_request_data(request_data)
            validation_passed = True
        except HTTPException as e:
            validation_passed = False
            error_detail = e.detail

        # Then
        assert validation_passed is False
        assert "필수 필드가 누락되었습니다" in error_detail
        assert "['id', 'buy_date', 'purchase_currency_type']" in error_detail

    def test_validate_request_data_success(self):
        # Given
        valid_request_data = UpdateAssetFieldRequest(
            root=["id", "buy_date", "purchase_currency_type", "quantity", "stock_name"]
        )

        # When
        try:
            UpdateAssetFieldRequest.validate_request_data(valid_request_data)
            validation_passed = True
        except HTTPException:
            validation_passed = False

        # Then
        assert validation_passed is True

    def test_validate_request_data_fail(self):
        # Given
        invalid_request_data = UpdateAssetFieldRequest(root=["id", "invalid_field", "quantity"])

        # When
        try:
            UpdateAssetFieldRequest.validate_request_data(invalid_request_data)
            validation_passed = True
        except HTTPException as e:
            validation_passed = False
            error_detail = e.detail

        # Then
        assert validation_passed is False
        assert "'invalid_field'은 올바른 필드가 아닙니다." in error_detail


class TestAssetStockResponse:
    async def test_validate_assets_empty(self, setup_asset):
        # Given
        empty_assets: list[Asset] = []

        # When
        response = AssetStockResponse.validate_assets(empty_assets)

        # Then
        expected_response = AssetStockResponse(
            stock_assets=[],
            total_asset_amount=0.0,
            total_invest_amount=0.0,
            total_profit_rate=0.0,
            total_profit_amount=0.0,
            total_dividend_amount=0.0,
        )

        assert response == expected_response

    async def test_validate_assets_non_empty(self, session, setup_asset):
        # Given
        non_empty_assets: list[Asset] = await AssetRepository.get_eager(session, DUMMY_USER_ID, AssetType.STOCK)

        # When
        response = AssetStockResponse.validate_assets(non_empty_assets)

        # Then
        assert response is None

    async def test_parse(
        self,
        session: AsyncSession,
        redis_client: Redis,
        setup_asset,
        setup_dividend,
        setup_exchange_rate,
        setup_realtime_stock_price,
        setup_stock_daily,
        setup_asset_field,
    ):
        # Given
        assets: list[Asset] = await AssetRepository.get_eager(session, DUMMY_USER_ID, AssetType.STOCK)
        stock_daily_map = await StockDailyService.get_map_range(session, assets)
        lastest_stock_daily_map = await StockDailyService.get_latest_map(session, assets)
        dividend_map = await DividendService.get_recent_map(session, assets)
        exchange_rate_map = await ExchangeRateService.get_exchange_rate_map(redis_client)
        current_stock_price_map = await StockService.get_current_stock_price(
            redis_client, lastest_stock_daily_map, assets
        )
        stock_assets = await AssetStockService.get_stock_assets(
            session, DUMMY_USER_ID, assets, stock_daily_map, current_stock_price_map, dividend_map, exchange_rate_map
        )
        total_asset_amount = AssetStockService.get_total_asset_amount(
            assets, current_stock_price_map, exchange_rate_map
        )
        total_invest_amount = AssetStockService.get_total_investment_amount(assets, stock_daily_map, exchange_rate_map)
        total_dividend_amount = DividendService.get_total_dividend(assets, dividend_map, exchange_rate_map)

        # When
        stock_asset_response = AssetStockResponse.parse(
            stock_assets=stock_assets,
            total_asset_amount=total_asset_amount,
            total_invest_amount=total_invest_amount,
            total_dividend_amount=total_dividend_amount,
        )

        # Then
        expected_profit_rate = ((total_asset_amount - total_invest_amount) / total_invest_amount) * 100
        assert stock_asset_response.total_profit_rate == pytest.approx(expected_profit_rate)

        expected_profit_amount = total_asset_amount - total_invest_amount
        assert stock_asset_response.total_profit_amount == pytest.approx(expected_profit_amount)

        assert len(stock_asset_response.stock_assets) == len(stock_assets)
