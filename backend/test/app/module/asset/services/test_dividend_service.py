import pytest
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.module.asset.enum import AssetType
from app.module.asset.model import Asset
from app.module.asset.repository.asset_repository import AssetRepository
from app.module.asset.services.dividend_service import DividendService
from app.module.asset.services.exchange_rate_service import ExchangeRateService
from app.module.auth.constant import DUMMY_USER_ID


class TestDividendService:
    async def test_get_recent_map(self, session: AsyncSession, setup_dividend, setup_asset):
        # Given
        assets = await session.execute(select(Asset).filter(Asset.user_id == DUMMY_USER_ID))
        assets = assets.scalars().all()

        # When
        result = await DividendService.get_recent_map(session, assets)

        # Then
        assert result["AAPL"] == 1.60
        assert result["TSLA"] == 0.90

    async def test_get_total_dividend(
        self, session: AsyncSession, redis_client: Redis, setup_exchange_rate, setup_asset, setup_dividend
    ):
        # Given
        assets: list[Asset] = await AssetRepository.get_eager(session, DUMMY_USER_ID, AssetType.STOCK)
        dividend_map = await DividendService.get_recent_map(session, assets)
        exchange_rate_map = await ExchangeRateService.get_exchange_rate_map(redis_client)

        # When
        total_dividend = DividendService.get_total_dividend(
            assets=assets,
            dividend_map=dividend_map,
            exchange_rate_map=exchange_rate_map,
        )

        # Then
        expected_total_dividend = 0.0
        for asset in assets:
            dividend_per_stock = dividend_map.get(asset.asset_stock.stock.code, 0.0)
            exchange_rate = ExchangeRateService.get_won_exchange_rate(asset, exchange_rate_map)
            expected_total_dividend += dividend_per_stock * asset.asset_stock.quantity * exchange_rate

        assert total_dividend == pytest.approx(expected_total_dividend)
