from datetime import date

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.model import Asset, Stock, StockDaily
from app.module.asset.redis_repository import RedisRealTimeStockRepository
from app.module.asset.repository.stock_repository import StockRepository


class StockService:
    @staticmethod
    async def get_stock_map(session: AsyncSession, stock_code: str) -> dict[str, Stock] | None:
        stock = await StockRepository.get_by_code(session, stock_code)
        return {stock.code: stock} if stock else None

    @staticmethod
    def check_not_found_stock(
        stock_daily_map: dict[tuple[str, date], StockDaily],
        current_stock_daily_map: dict[str, float] | dict[str, None],
        dummy_assets: list[Asset],
    ) -> list[str]:
        result = []
        for asset in dummy_assets:
            stock_daily = stock_daily_map.get((asset.asset_stock.stock.code, asset.asset_stock.purchase_date))
            current_stock_daily = current_stock_daily_map.get(asset.asset_stock.stock.code)
            if stock_daily is None or current_stock_daily is None:
                result.append(asset.asset_stock.stock.code)
                continue
        return result

    @staticmethod
    async def get_current_stock_price(
        redis_client: Redis, lastest_stock_daily_map: dict[str, StockDaily], assets: list[Asset]
    ) -> dict[str, float]:
        stock_codes = [asset.asset_stock.stock.code for asset in assets]
        current_prices = await RedisRealTimeStockRepository.bulk_get(redis_client, stock_codes)

        result = {}
        for i, stock_code in enumerate(stock_codes):
            current_price = current_prices[i]
            if current_price is None:
                stock_daily = lastest_stock_daily_map.get(stock_code)
                current_price = stock_daily.adj_close_price if stock_daily else 0.0

            result[stock_code] = float(current_price)
        return result

    @staticmethod
    async def get_current_stock_price_by_code(
        redis_client: Redis, lastest_stock_daily_map: dict[str, StockDaily], stock_codes: list[str]
    ) -> dict[str, float]:
        current_prices = await RedisRealTimeStockRepository.bulk_get(redis_client, stock_codes)

        result = {}
        for i, stock_code in enumerate(stock_codes):
            current_price = current_prices[i]
            if current_price is None:
                stock_daily = lastest_stock_daily_map.get(stock_code)
                current_price = stock_daily.adj_close_price if stock_daily else 0.0

            result[stock_code] = float(current_price)
        return result

    @staticmethod
    def get_daily_profit(
        lastest_stock_daily_map: dict[str, StockDaily],
        current_stock_price_map: dict[str, float],
        stock_codes: list[str],
    ) -> dict[str, float]:
        result = {}
        for stock_code in stock_codes:
            stock_daily = lastest_stock_daily_map.get(stock_code)
            current_stock_price = current_stock_price_map.get(stock_code)
            if current_stock_price is None or stock_daily is None:
                continue

            stock_profit = ((current_stock_price - stock_daily.adj_close_price) / stock_daily.adj_close_price) * 100
            result[stock_code] = stock_profit
        return result
