import datetime

from app.common.util.time import end_timestamp, start_timestamp
from app.module.asset.enum import Country, CountryMarketCode, MarketIndex
from app.module.asset.model import (  # noqa: F401 > relationship 설정시 필요합니다.
    Asset,
    AssetStock,
    Dividend,
    Stock,
    StockDaily,
    StockMonthly,
    StockWeekly,
)
from app.module.auth.model import User  # noqa: F401 > relationship 설정시 필요합니다.


def get_last_week_period_bounds() -> tuple[int, int]:
    now = datetime.datetime.now()
    seven_days_ago = now - datetime.timedelta(days=7)

    start_period = int(seven_days_ago.timestamp())
    end_period = int(now.timestamp())

    return start_period, end_period


def get_period_bounds(stock_history_timerange: int) -> tuple[int, int]:
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    start_year = current_year - stock_history_timerange

    return start_timestamp(start_year, current_month), end_timestamp(current_year, current_month)


def format_stock_code(code: str, country: Country, market_index: MarketIndex) -> str:
    if country == Country.USA:
        return code
    elif country == Country.KOREA:
        if market_index == MarketIndex.KOSPI:
            return f"{code}.{CountryMarketCode.KOREA_KOSPI}"
        else:
            return f"{code}.{CountryMarketCode.KOREA_KOSDAQ}"
    elif country == Country.JAPAN:
        return f"{code}.{CountryMarketCode.JAPAN}"
    elif country == Country.AUSTRALIA:
        return f"{code}.{CountryMarketCode.AUSTRALIA}"
    elif country == Country.BRAZIL:
        return f"{code}.{CountryMarketCode.BRAZIL}"
    elif country == Country.CANADA:
        return f"{code}.{CountryMarketCode.CANADA}"
    elif country == Country.CHINA:
        return f"{code}.{CountryMarketCode.CHINA}"
    elif country == Country.FRANCE:
        return f"{code}.{CountryMarketCode.FRANCE}"
    elif country == Country.GERMANY:
        return f"{code}.{CountryMarketCode.GERMANY}"
    elif country == Country.HONGKONG:
        return f"{code}.{CountryMarketCode.HONGKONG}"
    elif country == Country.INDIA:
        return f"{code}.{CountryMarketCode.INDIA}"
    elif country == Country.ITALY:
        return f"{code}.{CountryMarketCode.ITALY}"
    elif country == Country.NETHERLAND:
        return f"{code}.{CountryMarketCode.NETHERLAND}"
    elif country == Country.SPAIN:
        return f"{code}.{CountryMarketCode.SPAIN}"
    elif country == Country.SWITZERLAND:
        return f"{code}.{CountryMarketCode.SWITZERLAND}"
    elif country == Country.UK:
        return f"{code}.{CountryMarketCode.UK}"
    else:
        return f"{code}.{market_index.value}"
