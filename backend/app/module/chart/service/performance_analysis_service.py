import json
from collections import defaultdict
from datetime import date, datetime, time

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.enum import AssetType, MarketIndex
from app.module.asset.model import MarketIndexDaily, StockDaily, StockMinutely
from app.module.asset.repository.asset_repository import AssetRepository
from app.module.asset.repository.market_index_daily_repository import MarketIndexDailyRepository
from app.module.asset.repository.market_index_minutely_repository import MarketIndexMinutelyRepository
from app.module.asset.repository.stock_daily_repository import StockDailyRepository
from app.module.asset.repository.stock_minutely_repository import StockMinutelyRepository
from app.module.asset.services.asset_stock_service import AssetStockService
from app.module.asset.services.exchange_rate_service import ExchangeRateService
from app.module.asset.services.stock_service import StockService
from app.module.chart.enum import IntervalType
from app.module.chart.redis_repository import RedisMarketIndiceRepository


class PerformanceAnalysis:
    @staticmethod
    async def get_user_analysis_short(
        session: AsyncSession,
        redis_client: Redis,
        interval_start: datetime,
        interval_end: datetime,
        user_id: int,
        interval: IntervalType,
        market_analysis_result: dict[datetime, float],
    ) -> dict[datetime, float]:
        assets = await AssetRepository.get_eager_by_range(
            session, user_id, AssetType.STOCK, (interval_start, interval_end)
        )

        stock_code_date_pairs = [(asset.asset_stock.stock.code, asset.asset_stock.purchase_date) for asset in assets]
        stock_dailies: list[StockDaily] = await StockDailyRepository.get_stock_dailies_by_code_and_date(
            session, stock_code_date_pairs
        )
        stock_daily_map = {(daily.code, daily.date): daily for daily in stock_dailies}

        exchange_rate_map: dict[str, float] = await ExchangeRateService.get_exchange_rate_map(redis_client)

        stock_codes = [asset.asset_stock.stock.code for asset in assets]
        interval_data: list[StockMinutely] = await StockMinutelyRepository.get_by_range_interval_minute(
            session, (interval_start, interval_end), stock_codes, interval.get_interval()
        )

        stock_interval_date_price_map = {
            f"{stock_minutely.code}_{stock_minutely.datetime}": stock_minutely.current_price
            for stock_minutely in interval_data
        }

        assets_by_date = defaultdict(list)
        for asset in assets:
            purchase_datetime = datetime.combine(asset.asset_stock.purchase_date, time.max)
            assets_by_date[purchase_datetime].append(asset)

        result = {}
        cumulative_assets = []

        for market_datetime in sorted(market_analysis_result):
            if market_datetime in assets_by_date:
                assets_for_date = assets_by_date[market_datetime]
                cumulative_assets.extend(assets_for_date)

            total_asset_amount = AssetStockService.get_total_asset_amount_minute(
                assets, stock_interval_date_price_map, exchange_rate_map, market_datetime
            )

            total_invest_amount = AssetStockService.get_total_investment_amount(
                cumulative_assets, stock_daily_map, exchange_rate_map
            )

            total_profit_rate = 0.0
            if total_invest_amount > 0:
                total_profit_rate = ((total_asset_amount - total_invest_amount) / total_invest_amount) * 100

            result[market_datetime] = total_profit_rate

        return result

    @staticmethod
    async def get_user_analysis(
        session: AsyncSession,
        redis_client: Redis,
        interval_start: date,
        interval_end: date,
        user_id: int,
        market_analysis_result: dict[date, float],
    ) -> dict[date, float]:
        assets = await AssetRepository.get_eager_by_range(
            session, user_id, AssetType.STOCK, (interval_start, interval_end)
        )

        stock_codes = [asset.asset_stock.stock.code for asset in assets]
        stock_code_date_pairs = [(asset.asset_stock.stock.code, asset.asset_stock.purchase_date) for asset in assets]

        stock_dailies: list[StockDaily] = await StockDailyRepository.get_stock_dailies_by_code_and_date(
            session, stock_code_date_pairs
        )
        stock_daily_map = {(daily.code, daily.date): daily for daily in stock_dailies}

        latest_stock_dailies: list[StockDaily] = await StockDailyRepository.get_latest(session, stock_codes)
        latest_stock_daily_map = {daily.code: daily for daily in latest_stock_dailies}

        current_stock_price_map = await StockService.get_current_stock_price_by_code(
            redis_client, latest_stock_daily_map, stock_codes
        )
        exchange_rate_map = await ExchangeRateService.get_exchange_rate_map(redis_client)

        assets_by_date = defaultdict(list)
        for asset in assets:
            assets_by_date[asset.asset_stock.purchase_date].append(asset)

        cumulative_assets = []
        result = {}

        for market_date in sorted(market_analysis_result):
            if market_date in assets_by_date:
                assets_for_date = assets_by_date[market_date]
                cumulative_assets.extend(assets_for_date)

            total_asset_amount = AssetStockService.get_total_asset_amount(
                cumulative_assets, current_stock_price_map, exchange_rate_map
            )
            total_invest_amount = AssetStockService.get_total_investment_amount(
                cumulative_assets, stock_daily_map, exchange_rate_map
            )

            total_profit_rate = 0.0
            if total_invest_amount > 0:
                total_profit_rate = ((total_asset_amount - total_invest_amount) / total_invest_amount) * 100

            result[market_date] = total_profit_rate

        return result

    @staticmethod
    async def get_market_analysis_short(
        session: AsyncSession,
        redis_client: Redis,
        interval_start: datetime,
        interval_end: datetime,
        interval: IntervalType,
    ) -> dict[datetime, float]:
        market_data: list[MarketIndexDaily] = await MarketIndexMinutelyRepository.get_by_range_interval_minute(
            session, (interval_start, interval_end), MarketIndex.KOSPI, interval.get_interval()
        )

        current_kospi_price_raw = await RedisMarketIndiceRepository.get(redis_client, MarketIndex.KOSPI)
        if current_kospi_price_raw is None:
            return {}
        current_kospi_price_json = json.loads(current_kospi_price_raw)
        current_kospi_price = float(current_kospi_price_json["current_value"])

        result = {}

        for market_index in market_data:
            profit = ((current_kospi_price - market_index.current_price) / market_index.current_price) * 100

            result[market_index.datetime] = profit

        return result

    @staticmethod
    async def get_market_analysis(
        session: AsyncSession, redis_client: Redis, interval_start: date, interval_end: date
    ) -> dict[date, float]:
        market_data: list[MarketIndexDaily] = await MarketIndexDailyRepository.get_by_range(
            session, (interval_start, interval_end), MarketIndex.KOSPI
        )

        current_kospi_price_raw = await RedisMarketIndiceRepository.get(redis_client, MarketIndex.KOSPI)
        current_kospi_price_json = json.loads(current_kospi_price_raw)
        current_kospi_price = float(current_kospi_price_json["current_value"])

        result = {}

        for market_index in market_data:
            profit = ((current_kospi_price - market_index.close_price) / market_index.close_price) * 100
            result[market_index.date] = profit

        return result
