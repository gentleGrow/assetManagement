from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.model import Asset, StockDaily
from app.module.asset.repository.stock_daily_repository import StockDailyRepository


class StockDailyService:
    @staticmethod
    async def get_latest_map(session: AsyncSession, assets: list[Asset]) -> dict[str, StockDaily]:
        stock_codes = [asset.asset_stock.stock.code for asset in assets]
        lastest_stock_dailies: list[StockDaily] = await StockDailyRepository.get_latest(session, stock_codes)
        return {daily.code: daily for daily in lastest_stock_dailies}

    @staticmethod
    async def get_map_range(session: AsyncSession, assets: list[Asset]) -> dict[tuple[str, date], StockDaily]:
        stock_code_date_pairs = [(asset.asset_stock.stock.code, asset.asset_stock.purchase_date) for asset in assets]
        stock_dailies: list[StockDaily] = await StockDailyRepository.get_stock_dailies_by_code_and_date(
            session, stock_code_date_pairs
        )

        return {(daily.code, daily.date): daily for daily in stock_dailies}
