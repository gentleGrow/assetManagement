from redis.asyncio import Redis

from app.module.asset.constant import CURRENCY_PAIRS
from app.module.asset.enum import CurrencyType
from app.module.asset.model import Asset, Dividend, StockDaily
from app.module.asset.schema.stock_schema import StockAsset
from database.redis import RedisExchangeRateRepository, RedisRealTimeStockRepository


async def get_exchange_rate_map(redis_client: Redis) -> dict[str, float]:
    result = {}

    keys = [f"{source_currency}_{target_currency}" for source_currency, target_currency in CURRENCY_PAIRS]

    exchange_rates: list[float] = await RedisExchangeRateRepository.bulk_get(redis_client, keys)

    for i, key in enumerate(keys):
        rate = exchange_rates[i]

        if rate is None:
            result[key] = 0.0
        else:
            result[key] = rate

    return result


def get_exchange_rate(source: CurrencyType, target: CurrencyType, exchange_rate_map: dict[str, float]) -> float:
    if source == target:
        return 1.0

    exchange_key = source + "_" + target
    result = exchange_rate_map.get(exchange_key)

    if result is not None:
        return float(result)
    else:
        return 0.0


async def get_current_stock_price(
    redis_client: Redis, stock_daily_map: dict[tuple[str, str], StockDaily], stock_codes: list[str]
) -> dict[str, float]:
    result = {}

    current_prices = await RedisRealTimeStockRepository.bulk_get(redis_client, stock_codes)

    for i, stock_code in enumerate(stock_codes):
        current_price = current_prices[i]

        if current_price is None:
            latest_date = max([date for (code, date) in stock_daily_map.keys() if code == stock_code], default=None)

            stock_daily = stock_daily_map.get((stock_code, latest_date))
            current_price = stock_daily.adj_close_price if stock_daily else 0.0

        result[stock_code] = float(current_price)
    return result


def check_not_found_stock(
    stock_daily_map: dict[tuple[str, str], StockDaily],
    current_stock_daily_map: dict[str, float],
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


def get_stock_assets(
    assets: list[Asset],
    stock_daily_map: dict[tuple[str, str], StockDaily],
    current_stock_price_map: dict[str, float],
    dividend_map: dict[str, Dividend],
    base_currency: bool,
    exchange_rate_map: dict[str, float],
) -> list[StockAsset]:
    stock_assets = []

    for asset in assets:
        stock_daily = stock_daily_map.get((asset.asset_stock.stock.code, asset.asset_stock.purchase_date))
        current_price = current_stock_price_map.get(asset.asset_stock.stock.code)

        if not stock_daily or not current_price:
            continue

        dividend_instance = dividend_map.get(asset.asset_stock.stock.code)
        dividend = dividend_instance.dividend if dividend_instance else 0

        purchase_price = (
            asset.asset_stock.purchase_price
            if asset.asset_stock.purchase_price is not None
            else stock_daily.adj_close_price
        )

        profit_rate = ((current_price - purchase_price) / purchase_price) * 100
        source_country = asset.asset_stock.stock.country.upper()
        source_currency = CurrencyType[source_country]
        won_exchange_rate = get_exchange_rate(source_currency, CurrencyType.KOREA, exchange_rate_map)

        if base_currency:
            current_price = current_price * won_exchange_rate
            opening_price = stock_daily.opening_price * won_exchange_rate
            highest_price = stock_daily.highest_price * won_exchange_rate
            lowest_price = stock_daily.lowest_price * won_exchange_rate
            purchase_price *= won_exchange_rate
            dividend *= won_exchange_rate
        else:
            current_price = current_price
            opening_price = stock_daily.opening_price
            highest_price = stock_daily.highest_price
            lowest_price = stock_daily.lowest_price
            purchase_price = purchase_price

        purchase_amount = purchase_price * asset.asset_stock.quantity

        stock_asset = StockAsset(
            id=asset.id,
            account_type=asset.asset_stock.account_type,
            buy_date=asset.asset_stock.purchase_date,
            current_price=current_price,
            dividend=dividend * asset.asset_stock.quantity,
            highest_price=highest_price,
            investment_bank=asset.asset_stock.investment_bank,
            lowest_price=lowest_price,
            opening_price=opening_price,
            profit_rate=profit_rate,
            profit_amount=current_price - purchase_price,
            purchase_amount=purchase_amount,
            purchase_price=purchase_price,
            purchase_currency_type=asset.asset_stock.purchase_currency_type,
            quantity=asset.asset_stock.quantity,
            stock_code=asset.asset_stock.stock.code,
            stock_name=asset.asset_stock.stock.name,
            stock_volume=stock_daily.trade_volume,
        )

        stock_assets.append(stock_asset)

    return stock_assets


def get_asset_stock_totals(
    assets: list[Asset],
    stock_daily_map: dict[tuple[str, str], StockDaily],
    current_stock_price_map: dict[str, float],
    dividend_map: dict[str, Dividend],
    base_currency: bool,
    exchange_rate_map: dict[str, float],
) -> tuple[float, float, float]:
    total_asset_amount = 0
    total_invest_amount = 0
    total_dividend_amount = 0

    for asset in assets:
        stock_daily = stock_daily_map.get((asset.asset_stock.stock.code, asset.asset_stock.purchase_date))
        current_price = current_stock_price_map.get(asset.asset_stock.stock.code)

        if not stock_daily or not current_price:
            continue

        dividend_instance = dividend_map.get(asset.asset_stock.stock.code)
        dividend = dividend_instance.dividend if dividend_instance else 0

        purchase_price = (
            asset.asset_stock.purchase_price
            if asset.asset_stock.purchase_price is not None
            else stock_daily.adj_close_price
        )

        source_country = asset.asset_stock.stock.country.upper()
        source_currency = CurrencyType[source_country]
        won_exchange_rate = get_exchange_rate(source_currency, CurrencyType.KOREA, exchange_rate_map)

        if base_currency:
            current_price = current_price * won_exchange_rate
            purchase_price *= won_exchange_rate
            dividend *= won_exchange_rate

        total_dividend_amount += dividend
        total_asset_amount += current_price * asset.asset_stock.quantity
        total_invest_amount += stock_daily.adj_close_price * asset.asset_stock.quantity

    return total_asset_amount, total_invest_amount, total_dividend_amount
