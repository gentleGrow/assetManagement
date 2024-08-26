from unittest.mock import AsyncMock

import pytest

from app.module.asset.constant import CURRENCY_PAIRS
from app.module.asset.enum import CurrencyType
from app.module.asset.service import (
    check_not_found_stock,
    get_asset_stock_totals,
    get_current_stock_price,
    get_exchange_rate,
    get_exchange_rate_map,
    get_stock_assets,
)


class TestAssetStock:
    @pytest.mark.asyncio
    async def test_get_exchange_rate_map(self, mock_source_to_target_exchange_rate):
        redis_client = AsyncMock()

        assert len(mock_source_to_target_exchange_rate) == len(CURRENCY_PAIRS)

        redis_client.mget.return_value = mock_source_to_target_exchange_rate

        exchange_rate_map = await get_exchange_rate_map(redis_client)

        expected_keys = [f"{pair[0].value}_{pair[1].value}" for pair in CURRENCY_PAIRS]

        assert isinstance(exchange_rate_map, dict)
        assert len(exchange_rate_map) == len(CURRENCY_PAIRS)
        assert all(isinstance(k, str) and isinstance(v, float) for k, v in exchange_rate_map.items())

        for i, key in enumerate(expected_keys):
            assert exchange_rate_map[key] == mock_source_to_target_exchange_rate[i]

    def test_get_exchange_rate(self, exchange_rate):
        rate = get_exchange_rate(CurrencyType.USA, CurrencyType.KOREA, exchange_rate)
        assert rate == 1200.0

        rate = get_exchange_rate(CurrencyType.KOREA, CurrencyType.USA, exchange_rate)
        assert rate == 0.00083

        rate = get_exchange_rate(CurrencyType.USA, CurrencyType.USA, exchange_rate)
        assert rate == 1.0

        rate = get_exchange_rate(CurrencyType.USA, CurrencyType.EUROPE, exchange_rate)
        assert rate == 0.0

    @pytest.mark.asyncio
    async def test_get_current_stock_price(self, current_stock_daily_map):
        redis_client = AsyncMock()
        stock_codes = ["AAPL", "GOOGL"]

        redis_client.mget.return_value = [155.0, 2800.0]

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("app.module.asset.service.RedisRealTimeStockRepository.bulk_get", redis_client.mget)

            current_prices = await get_current_stock_price(redis_client, current_stock_daily_map, stock_codes)

            assert isinstance(current_prices, dict)
            assert current_prices["AAPL"] == 155.0
            assert current_prices["GOOGL"] == 2800.0

    def test_check_not_found_stock(self, stock_dailies, dummy_assets, current_stock_price_map):
        stock_daily_map = {(daily.code, daily.date): daily for daily in stock_dailies}
        not_found_stock_codes = check_not_found_stock(stock_daily_map, current_stock_price_map, dummy_assets)

        assert len(not_found_stock_codes) == 0

    def test_get_stock_assets(self, dummy_assets, current_stock_daily_map, current_stock_price_map, dividends):
        exchange_rate_map = {
            "USD_KRW": 1200.0,
        }

        stock_assets = get_stock_assets(
            dummy_assets,
            current_stock_daily_map,
            current_stock_price_map,
            {dividend.stock_code: dividend for dividend in dividends},
            base_currency=True,
            exchange_rate_map=exchange_rate_map,
        )

        assert len(stock_assets) == len(dummy_assets)
        assert all(asset.current_price > 0 for asset in stock_assets)
        assert all(isinstance(asset.profit_rate, float) for asset in stock_assets)

    def test_get_asset_stock_totals(self, dummy_assets, current_stock_daily_map, current_stock_price_map, dividends):
        exchange_rate_map = {
            "USD_KRW": 1200.0,
        }

        total_asset_amount, total_invest_amount, total_dividend_amount = get_asset_stock_totals(
            dummy_assets,
            current_stock_daily_map,
            current_stock_price_map,
            {dividend.stock_code: dividend for dividend in dividends},
            base_currency=True,
            exchange_rate_map=exchange_rate_map,
        )

        assert total_asset_amount > 0
        assert total_invest_amount > 0
        assert total_dividend_amount > 0
