from datetime import date

import pytest
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.enum import AccountType, AssetType, InvestmentBankType, PurchaseCurrencyType, StockAsset
from app.module.asset.model import Asset, AssetField, AssetStock, Dividend, Stock, StockDaily
from app.module.auth.constant import DUMMY_NAME, DUMMY_USER_ID
from app.module.auth.enum import ProviderEnum, UserRoleEnum
from app.module.auth.model import User  # noqa: F401 > relationship 설정시 필요합니다.


@pytest.fixture(scope="function")
async def setup_asset_field(session: AsyncSession, setup_user, setup_stock):
    fields_to_disable = ["stock_volume", "purchase_currency_type", "purchase_price", "purchase_amount"]
    field_preference = [field for field in [field.value for field in StockAsset] if field not in fields_to_disable]
    asset_field = AssetField(user_id=DUMMY_USER_ID, field_preference=field_preference)

    session.add(asset_field)
    await session.commit()


@pytest.fixture(scope="function")
async def setup_realtime_stock_price(redis_client: Redis):
    keys = ["AAPL", "TSLA", "005930"]
    values = ["220.0", "230.0", "70000.0"]
    await redis_client.mset({key: value for key, value in zip(keys, values)})
    yield keys, values
    await redis_client.flushall()


@pytest.fixture(scope="function")
async def setup_exchange_rate(redis_client: Redis):
    keys = ["USD_KRW", "KRW_USD"]
    values = ["1300.0", "0.00075"]
    await redis_client.mset({key: value for key, value in zip(keys, values)})
    yield keys, values
    await redis_client.flushall()


@pytest.fixture(scope="function")
async def setup_dividend(session: AsyncSession, setup_stock):
    dividend1 = Dividend(dividend=1.5, stock_code="AAPL", date=date(2024, 8, 13))

    dividend2 = Dividend(dividend=1.6, stock_code="AAPL", date=date(2024, 8, 14))

    dividend3 = Dividend(dividend=0.8, stock_code="TSLA", date=date(2024, 8, 13))

    dividend4 = Dividend(dividend=0.9, stock_code="TSLA", date=date(2024, 8, 14))

    dividend5 = Dividend(dividend=100.0, stock_code="005930", date=date(2024, 8, 13))

    dividend6 = Dividend(dividend=105.0, stock_code="005930", date=date(2024, 8, 14))

    session.add_all([dividend1, dividend2, dividend3, dividend4, dividend5, dividend6])
    await session.commit()


@pytest.fixture(scope="function")
async def setup_user(session: AsyncSession):
    user = User(
        id=DUMMY_USER_ID,
        social_id="test_social_id",
        provider=ProviderEnum.GOOGLE,
        role=UserRoleEnum.USER,
        nickname=DUMMY_NAME,
    )
    session.add(user)
    await session.commit()


@pytest.fixture(scope="function")
async def setup_stock(session: AsyncSession):
    stock_1 = Stock(id=1, code="AAPL", country="USA", market_index="NASDAQ", name="Apple Inc.")
    stock_2 = Stock(id=2, code="TSLA", country="USA", market_index="NASDAQ", name="Tesla Inc.")
    stock_3 = Stock(id=3, code="005930", country="KOREA", market_index="KOSPI", name="삼성전자")
    session.add_all([stock_1, stock_2, stock_3])
    await session.commit()


@pytest.fixture(scope="function")
async def setup_stock_daily(session: AsyncSession, setup_user, setup_stock):
    stock_daily_1 = StockDaily(
        adj_close_price=150.0,
        close_price=148.0,
        code="AAPL",
        date=date(2024, 8, 13),
        highest_price=152.0,
        lowest_price=147.0,
        opening_price=149.0,
        trade_volume=1000000,
    )

    stock_daily_2 = StockDaily(
        adj_close_price=151.0,
        close_price=149.0,
        code="AAPL",
        date=date(2024, 8, 14),
        highest_price=153.0,
        lowest_price=148.0,
        opening_price=150.0,
        trade_volume=1050000,
    )

    stock_daily_3 = StockDaily(
        adj_close_price=720.0,
        close_price=715.0,
        code="TSLA",
        date=date(2024, 8, 13),
        highest_price=730.0,
        lowest_price=710.0,
        opening_price=720.0,
        trade_volume=1500000,
    )

    stock_daily_4 = StockDaily(
        adj_close_price=725.0,
        close_price=720.0,
        code="TSLA",
        date=date(2024, 8, 14),
        highest_price=735.0,
        lowest_price=715.0,
        opening_price=725.0,
        trade_volume=1600000,
    )

    stock_daily_5 = StockDaily(
        adj_close_price=70000.0,
        close_price=70000.0,
        code="005930",
        date=date(2024, 8, 13),
        highest_price=71000.0,
        lowest_price=69000.0,
        opening_price=70500.0,
        trade_volume=1000,
    )

    stock_daily_6 = StockDaily(
        adj_close_price=72000.0,
        close_price=72000.0,
        code="005930",
        date=date(2024, 8, 14),
        highest_price=73000.0,
        lowest_price=71000.0,
        opening_price=71500.0,
        trade_volume=1500,
    )

    session.add_all([stock_daily_1, stock_daily_2, stock_daily_3, stock_daily_4, stock_daily_5, stock_daily_6])
    await session.commit()


@pytest.fixture(scope="function")
async def setup_asset(session: AsyncSession, setup_user, setup_stock):
    asset_stock1 = AssetStock(
        account_type=AccountType.ISA.value,
        investment_bank=InvestmentBankType.MIRAEASSET.value,
        purchase_currency_type=PurchaseCurrencyType.USA.value,
        purchase_date=date(2024, 8, 13),
        purchase_price=500.0,
        quantity=1,
        stock_id=1,
    )

    asset_stock2 = AssetStock(
        account_type=AccountType.PENSION.value,
        investment_bank=InvestmentBankType.TOSS.value,
        purchase_currency_type=PurchaseCurrencyType.KOREA.value,
        purchase_date=date(2024, 8, 14),
        purchase_price=1000.0,
        quantity=2,
        stock_id=2,
    )

    asset_stock3 = AssetStock(
        account_type=AccountType.REGULAR.value,
        investment_bank=InvestmentBankType.KB.value,
        purchase_currency_type=PurchaseCurrencyType.KOREA.value,
        purchase_date=date(2024, 8, 14),
        purchase_price=None,
        quantity=1,
        stock_id=3,
    )

    asset1 = Asset(asset_type=AssetType.STOCK.value, user_id=DUMMY_USER_ID, asset_stock=asset_stock1)
    asset2 = Asset(asset_type=AssetType.STOCK.value, user_id=DUMMY_USER_ID, asset_stock=asset_stock2)
    asset3 = Asset(asset_type=AssetType.STOCK.value, user_id=DUMMY_USER_ID, asset_stock=asset_stock3)
    session.add_all([asset1, asset2, asset3])
    await session.commit()


@pytest.fixture(scope="function")
async def setup_all(
    setup_asset_field,
    setup_realtime_stock_price,
    setup_exchange_rate,
    setup_dividend,
    setup_user,
    setup_stock,
    setup_stock_daily,
    setup_asset,
):
    pass
