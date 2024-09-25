import pytest
from redis.asyncio import Redis

from app.module.asset.enum import AssetType, CurrencyType
from app.module.asset.model import Asset
from app.module.asset.repository.asset_repository import AssetRepository
from app.module.asset.services.exchange_rate_service import ExchangeRateService
from app.module.auth.constant import DUMMY_USER_ID


class TestExchangeRateService:
    @pytest.mark.asyncio
    async def test_get_dollar_exchange_rate_for_foreign_asset(
        self, session, redis_client, setup_exchange_rate, setup_asset
    ):
        # Given
        assets: list[Asset] = await AssetRepository.get_eager(session, DUMMY_USER_ID, AssetType.STOCK)
        exchange_rate_map = await ExchangeRateService.get_exchange_rate_map(redis_client)

        foreign_assets = [asset for asset in assets if asset.asset_stock.stock.country.upper().strip() != "USA"]
        test_asset = foreign_assets[0]

        # When
        dollar_exchange_rate = ExchangeRateService.get_dollar_exchange_rate(test_asset, exchange_rate_map)

        # Then
        expected_currency = CurrencyType[test_asset.asset_stock.stock.country.upper().strip()]
        expected_exchange_rate_key = f"{expected_currency}_{CurrencyType.USA}"
        expected_rate = float(exchange_rate_map.get(expected_exchange_rate_key, 0.0))
        assert dollar_exchange_rate == expected_rate

    @pytest.mark.asyncio
    async def test_get_dollar_exchange_rate_for_dollar_asset(
        self, session, redis_client, setup_exchange_rate, setup_asset
    ):
        # Given
        assets: list[Asset] = await AssetRepository.get_eager(session, DUMMY_USER_ID, AssetType.STOCK)
        exchange_rate_map = await ExchangeRateService.get_exchange_rate_map(redis_client)

        usa_assets = [asset for asset in assets if asset.asset_stock.stock.country.upper().strip() == "USA"]
        test_asset = usa_assets[0]

        # When
        dollar_exchange_rate = ExchangeRateService.get_dollar_exchange_rate(test_asset, exchange_rate_map)

        # Then
        assert dollar_exchange_rate == 1.0

    @pytest.mark.asyncio
    async def test_get_won_exchange_rate_for_korean_asset(
        self, session, redis_client, setup_exchange_rate, setup_asset
    ):
        # Given
        assets: list[Asset] = await AssetRepository.get_eager(session, DUMMY_USER_ID, AssetType.STOCK)
        exchange_rate_map = await ExchangeRateService.get_exchange_rate_map(redis_client)

        korean_assets = [asset for asset in assets if asset.asset_stock.stock.country.upper().strip() == "KOREA"]
        test_asset = korean_assets[0]

        # When
        won_exchange_rate = ExchangeRateService.get_won_exchange_rate(test_asset, exchange_rate_map)

        # Then
        assert won_exchange_rate == 1.0, "Expected exchange rate to be 1.0 for Korean assets"

    @pytest.mark.asyncio
    async def test_get_won_exchange_rate_for_foreign_asset(
        self, session, redis_client, setup_exchange_rate, setup_asset
    ):
        # Given
        assets: list[Asset] = await AssetRepository.get_eager(session, DUMMY_USER_ID, AssetType.STOCK)
        exchange_rate_map = await ExchangeRateService.get_exchange_rate_map(redis_client)

        foreign_assets = [asset for asset in assets if asset.asset_stock.stock.country.upper().strip() != "KOREA"]
        test_asset = foreign_assets[0]

        # When
        won_exchange_rate = ExchangeRateService.get_won_exchange_rate(test_asset, exchange_rate_map)

        # Then
        expected_currency = CurrencyType[test_asset.asset_stock.stock.country.upper().strip()]
        expected_exchange_rate_key = f"{expected_currency}_{CurrencyType.KOREA}"
        expected_rate = float(exchange_rate_map.get(expected_exchange_rate_key, 0.0))
        assert won_exchange_rate == expected_rate

    async def test_get_exchange_rate_map(self, redis_client: Redis, setup_exchange_rate):
        # Given
        expected_keys, expected_values = setup_exchange_rate

        # When
        exchange_rate_map = await ExchangeRateService.get_exchange_rate_map(redis_client)

        # Then
        for key, value in zip(expected_keys, expected_values):
            assert exchange_rate_map[key] == float(value)
