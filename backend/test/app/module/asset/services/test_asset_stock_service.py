from datetime import date

import pytest
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.enum import AccountType, AssetType, InvestmentBankType, PurchaseCurrencyType, StockAsset
from app.module.asset.model import Asset
from app.module.asset.repository.asset_repository import AssetRepository
from app.module.asset.schema import AssetStockPostRequest
from app.module.asset.services.asset_stock_service import AssetStockService
from app.module.asset.services.dividend_service import DividendService
from app.module.asset.services.exchange_rate_service import ExchangeRateService
from app.module.asset.services.stock_daily_service import StockDailyService
from app.module.asset.services.stock_service import StockService
from app.module.auth.constant import DUMMY_USER_ID


class TestAssetStockService:
    async def test_save_asset_stock_by_post(self, session: AsyncSession, setup_stock, setup_stock_daily, setup_user):
        # Given
        stock_id = 1

        request_data = AssetStockPostRequest(
            buy_date=date(2024, 8, 13),
            purchase_currency_type=PurchaseCurrencyType.USA,
            quantity=10,
            stock_code="AAPL",
            account_type=AccountType.ISA,
            investment_bank=InvestmentBankType.KB,
            purchase_price=500.0,
        )

        # When
        await AssetStockService.save_asset_stock_by_post(session, request_data, stock_id, DUMMY_USER_ID)
        saved_assets = await AssetRepository.get_eager(session, DUMMY_USER_ID, AssetType.STOCK)

        # Then
        assert len(saved_assets) == 1
        assert saved_assets[0].asset_stock.stock_id == stock_id

    async def test_get_total_investment_amount(
        self, session: AsyncSession, redis_client: Redis, setup_asset, setup_exchange_rate, setup_stock_daily
    ):
        # Given
        assets: list[Asset] = await AssetRepository.get_eager(session, DUMMY_USER_ID, AssetType.STOCK)
        exchange_rate_map = await ExchangeRateService.get_exchange_rate_map(redis_client)
        stock_daily_map = await StockDailyService.get_map_range(session, assets)

        # When
        total_investment_amount = AssetStockService.get_total_investment_amount(
            assets=assets,
            stock_daily_map=stock_daily_map,
            exchange_rate_map=exchange_rate_map,
        )

        # Then
        expected_total_investment_amount = 0.0
        for asset in assets:
            stock_daily = stock_daily_map.get((asset.asset_stock.stock.code, asset.asset_stock.purchase_date), None)
            if stock_daily is None:
                continue

            if asset.asset_stock.purchase_currency_type == PurchaseCurrencyType.USA:
                invest_price = (
                    asset.asset_stock.purchase_price
                    * ExchangeRateService.get_won_exchange_rate(asset, exchange_rate_map)
                    if asset.asset_stock.purchase_price
                    else stock_daily.adj_close_price
                    * ExchangeRateService.get_won_exchange_rate(asset, exchange_rate_map)
                )
            else:
                invest_price = (
                    asset.asset_stock.purchase_price
                    if asset.asset_stock.purchase_price
                    else stock_daily.adj_close_price
                )

            expected_total_investment_amount += invest_price * asset.asset_stock.quantity

        assert total_investment_amount == pytest.approx(expected_total_investment_amount)

    async def test_get_total_asset_amount(
        self,
        session: AsyncSession,
        redis_client: Redis,
        setup_asset,
        setup_realtime_stock_price,
        setup_exchange_rate,
    ):
        # Given
        assets: list[Asset] = await AssetRepository.get_eager(session, DUMMY_USER_ID, AssetType.STOCK)
        lastest_stock_daily_map = await StockDailyService.get_latest_map(session, assets)
        current_stock_price_map = await StockService.get_current_stock_price(
            redis_client, lastest_stock_daily_map, assets
        )
        exchange_rate_map = await ExchangeRateService.get_exchange_rate_map(redis_client)

        # When
        total_asset_amount = AssetStockService.get_total_asset_amount(
            assets=assets,
            current_stock_price_map=current_stock_price_map,
            exchange_rate_map=exchange_rate_map,
        )

        # Then
        expected_total_asset_amount = 0.0
        for asset in assets:
            current_price = current_stock_price_map.get(asset.asset_stock.stock.code)
            exchange_rate = ExchangeRateService.get_won_exchange_rate(asset, exchange_rate_map)
            expected_total_asset_amount += current_price * asset.asset_stock.quantity * exchange_rate

        assert total_asset_amount == pytest.approx(expected_total_asset_amount)

    async def test_get_stock_assets(
        self,
        session: AsyncSession,
        redis_client: Redis,
        setup_asset,
        setup_dividend,
        setup_exchange_rate,
        setup_realtime_stock_price,
        setup_stock,
        setup_stock_daily,
        setup_user,
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

        # When
        stock_assets: list[dict] = await AssetStockService.get_stock_assets(
            session=session,
            user_id=DUMMY_USER_ID,
            assets=assets,
            stock_daily_map=stock_daily_map,
            current_stock_price_map=current_stock_price_map,
            dividend_map=dividend_map,
            exchange_rate_map=exchange_rate_map,
        )

        # Then
        expected_exchange_rate_aapl: float = (
            ExchangeRateService.get_dollar_exchange_rate(assets[0], exchange_rate_map)
            if assets[0].asset_stock.purchase_currency_type == PurchaseCurrencyType.USA
            else ExchangeRateService.get_won_exchange_rate(assets[0], exchange_rate_map)
        )

        stock_asset_aapl = next(asset for asset in stock_assets if asset[StockAsset.STOCK_CODE.value] == "AAPL")
        assert stock_asset_aapl[StockAsset.STOCK_NAME.value] == "Apple Inc."
        assert stock_asset_aapl[StockAsset.CURRENT_PRICE.value] == 220.0 * expected_exchange_rate_aapl
        assert (
            stock_asset_aapl[StockAsset.DIVIDEND.value]
            == 1.6 * stock_asset_aapl[StockAsset.QUANTITY.value] * expected_exchange_rate_aapl
        )
        assert stock_asset_aapl[StockAsset.PROFIT_RATE.value] == pytest.approx(
            ((220.0 * expected_exchange_rate_aapl - 500.0) / 500.0) * 100
        )
        assert stock_asset_aapl.get(StockAsset.PURCHASE_PRICE.value) is None

        stock_asset_tsla = next(asset for asset in stock_assets if asset[StockAsset.STOCK_CODE.value] == "TSLA")
        expected_exchange_rate_tsla: float = (
            ExchangeRateService.get_dollar_exchange_rate(assets[1], exchange_rate_map)
            if assets[1].asset_stock.purchase_currency_type == PurchaseCurrencyType.USA
            else ExchangeRateService.get_won_exchange_rate(assets[1], exchange_rate_map)
        )
        assert stock_asset_tsla[StockAsset.STOCK_NAME.value] == "Tesla Inc."
        assert stock_asset_tsla[StockAsset.CURRENT_PRICE.value] == 230.0 * expected_exchange_rate_tsla
        assert (
            stock_asset_tsla[StockAsset.DIVIDEND.value]
            == 0.9 * stock_asset_tsla[StockAsset.QUANTITY.value] * expected_exchange_rate_tsla
        )

        stock_asset_samsung = next(asset for asset in stock_assets if asset[StockAsset.STOCK_CODE.value] == "005930")
        assert stock_asset_samsung[StockAsset.STOCK_NAME.value] == "삼성전자"
        assert stock_asset_samsung[StockAsset.CURRENT_PRICE.value] == 70000.0
        assert stock_asset_samsung[StockAsset.DIVIDEND.value] == 105.0
