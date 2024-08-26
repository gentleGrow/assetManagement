from enum import StrEnum


class PurchaseCurrencyType(StrEnum):
    KOREA = "KRW"
    USA = "USD"


class InvestmentBankType(StrEnum):
    TOSS = "토스증권"
    MIRAEASSET = "미래에셋증권"
    SAMSUNGINVESTMENT = "삼성투자증권"
    KOREAINVESTMENT = "한국투자증권"
    KB = "KB증권"
    DAISHIN = "대신증권"
    NH = "NH투자증권"
    SHINHANINVESTMENT = "신한투자증권"
    KIWOOM = "키움증권"


class AccountType(StrEnum):
    ISA = "ISA"
    IRP = "IRP"
    PENSION = "개인연금"
    REGULAR = "일반계좌"


class AssetType(StrEnum):
    STOCK = "stock"
    BOND = "bond"
    VIRTUAL_ASSET = "virtual_asset"
    CURRENCY = "currency"
    OTHER = "other"


class VirtualExchangeType(StrEnum):
    UPBIT = "upbit"
    BITHUMB = "bithumb"
    BINANCE = "binance"
    WALLET = "wallet"


class CurrencyType(StrEnum):
    KOREA = "KRW"
    USA = "USD"
    JAPAN = "JPY"
    AUSTRALIA = "AUD"
    BRAZIL = "BRL"
    CANADA = "CAD"
    CHINA = "CNY"
    EUROPE = "EUR"
    HONG_KONG = "HKD"
    INDIA = "INR"
    SWITZERLAND = "CHF"
    UNITED_KINGDOM = "GBP"


class TimeInterval(StrEnum):
    DAY = "1d"
    WEEK = "1wk"
    MONTH = "1mo"


class Country(StrEnum):
    USA = "USA"
    JAPAN = "JAPAN"
    UK = "UK"
    GERMANY = "GERMANY"
    FRANCE = "FRANCE"
    CHINA = "CHINA"
    HONGKONG = "HONGKONG"
    CANADA = "CANADA"
    AUSTRALIA = "AUSTRALIA"
    INDIA = "INDIA"
    SOUTH_KOREA = "SOUTH_KOREA"
    BRAZIL = "BRAZIL"
    RUSSIA = "RUSSIA"
    ITALY = "ITALY"
    SPAIN = "SPAIN"
    SWITZERLAND = "SWITZERLAND"
    NETHERLAND = "NETHERLAND"
    EUROZONE = "EUROZONE"
    KOREA = "KOREA"


class MarketIndex(StrEnum):
    NYSE = "NYSE"
    NASDAQ = "NASDAQ"
    DJIA = "DJIA"
    IXIC = "IXIC"
    N225 = "N225"
    FTSE = "FTSE"
    DAX = "DAX"
    PX1 = "PX1"
    SHCOMP = "SHCOMP"
    HSI = "HSI"
    GSPTSE = "GSPTSE"
    AXJO = "AXJO"
    NSEI = "NSEI"
    KS11 = "KS11"
    BVSP = "BVSP"
    IMOEX = "IMOEX"
    FTSEMIB = "FTSEMIB"
    IBEX = "IBEX"
    SMI = "SMI"
    AEX = "AEX"
    TSE = "TSE"
    SX5E = "SX5E"
    KOSPI = "KOSPI"
    KOSDAQ = "KOSDAQ"


class CountryMarketCode(StrEnum):
    USA = ""
    KOREA_KOSPI = "KS"
    KOREA_KOSDAQ = "KQ"
    JAPAN = "T"
    UK = "L"
    GERMANY = "DE"
    FRANCE = "PA"
    CHINA = "SS"
    HONGKONG = "HK"
    CANADA = "TO"
    AUSTRALIA = "AX"
    INDIA = "BO"
    BRAZIL = "SA"
    ITALY = "MI"
    SPAIN = "MC"
    SWITZERLAND = "SW"
    NETHERLAND = "AS"
