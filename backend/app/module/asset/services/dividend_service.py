from collections import defaultdict
from datetime import date

from pandas import to_datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.enum import CurrencyType
from app.module.asset.model import Asset, Dividend
from app.module.asset.repository.dividend_repository import DividendRepository
from app.module.asset.services.exchange_rate_service import ExchangeRateService


class DividendService:
    @staticmethod
    async def get_recent_map(session: AsyncSession, assets: list[Asset]) -> dict[str, float]:
        stock_codes = [asset.asset_stock.stock.code for asset in assets]
        dividends: list[Dividend] = await DividendRepository.get_dividends_recent(session, stock_codes)
        return {dividend.stock_code: dividend.dividend for dividend in dividends}

    @staticmethod
    async def get_composition(
        assets: list[Asset],
        exchange_rate_map: dict[str, float],
        dividend_map: dict[str, float],
    ) -> list[tuple[str, float, float]]:
        if len(assets) == 0:
            return []

        total_dividend: defaultdict[str, float] = defaultdict(float)
        total_dividend_sum = 0.0

        for asset in assets:
            source_country = asset.asset_stock.stock.country.upper().strip()
            source_currency = CurrencyType[source_country]

            won_exchange_rate = ExchangeRateService.get_exchange_rate(
                source_currency, CurrencyType.KOREA, exchange_rate_map
            )

            stock_code = asset.asset_stock.stock.code
            quantity = asset.asset_stock.quantity

            dividend = dividend_map.get(stock_code)

            if dividend is None:
                continue

            current_total_dividend = dividend * won_exchange_rate * quantity

            total_dividend[stock_code] += current_total_dividend
            total_dividend_sum += current_total_dividend

        return [
            (stock_code, dividend, (dividend / total_dividend_sum) * 100)
            for stock_code, dividend in total_dividend.items()
        ]

    @staticmethod
    def get_total_estimate_dividend(
        assets: list[Asset],
        exchange_rate_map: dict[str, float],
        dividend_map: dict[str, float],
    ) -> dict[str, float]:
        total_dividend_date: defaultdict[date, float] = defaultdict(float)

        for asset in assets:
            source_country = asset.asset_stock.stock.country.upper().strip()
            source_currency = CurrencyType[source_country]

            won_exchange_rate = ExchangeRateService.get_exchange_rate(
                source_currency, CurrencyType.KOREA, exchange_rate_map
            )

            stock_code = asset.asset_stock.stock.code
            purchase_date = asset.asset_stock.purchase_date
            quantity = asset.asset_stock.quantity

            last_dividend_date: date | None = None

            for key, dividend_amount in dividend_map.items():
                dividend_code, dividend_date_str = key.split("_")
                try:
                    dividend_date = to_datetime(dividend_date_str).date()

                    if dividend_code == stock_code and dividend_date >= purchase_date:
                        dividend_kr = dividend_amount * won_exchange_rate * quantity
                        total_dividend_date[dividend_date] += dividend_kr
                        last_dividend_date = dividend_date
                except Exception:
                    continue

            if last_dividend_date:
                last_year = last_dividend_date.year - 1
                last_year_dividend_date = last_dividend_date.replace(year=last_year)

                for key, dividend_amount in dividend_map.items():
                    dividend_code, dividend_date_str = key.split("_")
                    try:
                        dividend_date = to_datetime(dividend_date_str).date()
                        if (
                            dividend_code == stock_code
                            and dividend_date >= last_year_dividend_date
                            and dividend_date <= date(last_year, 12, 31)
                        ):
                            new_dividend_date = dividend_date.replace(year=last_dividend_date.year)
                            dividend_kr = dividend_amount * won_exchange_rate * quantity
                            total_dividend_date[new_dividend_date] += dividend_kr
                    except Exception:
                        continue

        return {dividend_date.isoformat(): amount for dividend_date, amount in total_dividend_date.items()}

    @staticmethod
    def get_total_dividend(
        assets: list[Asset], dividend_map: dict[str, float], exchange_rate_map: dict[str, float]
    ) -> float:
        total_dividend_amount = 0.0

        for asset in assets:
            total_dividend_amount += (
                dividend_map.get(asset.asset_stock.stock.code, 0.0)
                * asset.asset_stock.quantity
                * ExchangeRateService.get_won_exchange_rate(asset, exchange_rate_map)
            )

        return total_dividend_amount
