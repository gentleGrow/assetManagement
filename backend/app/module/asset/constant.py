from datetime import date

from app.module.asset.enum import AccountType, CurrencyType, InvestmentBankType, PurchaseCurrencyType

REDIS_STOCK_EXPIRE_SECOND = 60 * 60 * 24
DUMMY_ASSET_EXPIRE_SECOND = 60 * 60
DUMMY_ASSET_KOREA_KEY = "dummy_asset_korea"
DUMMY_ASSET_FOREIGN_KEY = "dummy_asset_foreign"

COUNTRY_TO_CURRENCY = {
    "KOREA": CurrencyType.KOREA,
    "USA": CurrencyType.USA,
    "JAPAN": CurrencyType.JAPAN,
    "AUSTRALIA": CurrencyType.AUSTRALIA,
    "BRAZIL": CurrencyType.BRAZIL,
    "CANADA": CurrencyType.CANADA,
    "CHINA": CurrencyType.CHINA,
    "EUROPE": CurrencyType.EUROPE,
    "HONG KONG": CurrencyType.HONG_KONG,
    "INDIA": CurrencyType.INDIA,
    "SWITZERLAND": CurrencyType.SWITZERLAND,
    "UNITED KINGDOM": CurrencyType.UNITED_KINGDOM,
}

CURRENCY_PAIRS = [
    (CurrencyType.USA, CurrencyType.KOREA),
    (CurrencyType.JAPAN, CurrencyType.KOREA),
    (CurrencyType.AUSTRALIA, CurrencyType.KOREA),
    (CurrencyType.BRAZIL, CurrencyType.KOREA),
    (CurrencyType.CANADA, CurrencyType.KOREA),
    (CurrencyType.CHINA, CurrencyType.KOREA),
    (CurrencyType.EUROPE, CurrencyType.KOREA),
    (CurrencyType.HONG_KONG, CurrencyType.KOREA),
    (CurrencyType.INDIA, CurrencyType.KOREA),
    (CurrencyType.SWITZERLAND, CurrencyType.KOREA),
    (CurrencyType.UNITED_KINGDOM, CurrencyType.KOREA),
    (CurrencyType.KOREA, CurrencyType.USA),
    (CurrencyType.JAPAN, CurrencyType.USA),
    (CurrencyType.AUSTRALIA, CurrencyType.USA),
    (CurrencyType.BRAZIL, CurrencyType.USA),
    (CurrencyType.CANADA, CurrencyType.USA),
    (CurrencyType.CHINA, CurrencyType.USA),
    (CurrencyType.EUROPE, CurrencyType.USA),
    (CurrencyType.HONG_KONG, CurrencyType.USA),
    (CurrencyType.INDIA, CurrencyType.USA),
    (CurrencyType.SWITZERLAND, CurrencyType.USA),
    (CurrencyType.UNITED_KINGDOM, CurrencyType.USA),
]


STOCK_CODES = ["005930", "AAPL", "7203", "446720", "005930"]  # 삼성전자, 애플, 토요타, ETF SOL 다우존스, 삼성전자

PURCHASE_DATES = [date(2015, 7, 22), date(2012, 11, 14), date(2020, 6, 8), date(2024, 5, 28), date(2016, 4, 14)]

INVESTMENT_BANKS = [
    InvestmentBankType.TOSS.value,
    InvestmentBankType.KB.value,
    InvestmentBankType.NH.value,
    InvestmentBankType.KIWOOM.value,
    InvestmentBankType.MIRAEASSET.value,
]


PURCHASECURRENCYTYPES = [
    PurchaseCurrencyType.KOREA.value,
    PurchaseCurrencyType.USA.value,
    PurchaseCurrencyType.KOREA.value,
    PurchaseCurrencyType.USA.value,
    PurchaseCurrencyType.KOREA.value,
]


ACCOUNT_TYPES = [
    AccountType.REGULAR.value,
    AccountType.REGULAR.value,
    AccountType.REGULAR.value,
    AccountType.ISA.value,
    AccountType.REGULAR.value,
]

STOCK_QUANTITIES = [6, 3, 2, 4, 5]
