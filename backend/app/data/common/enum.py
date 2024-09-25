from enum import StrEnum


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


class MarketIndexEnum(StrEnum):
    NASDAQ = "^IXIC"
    SP_500 = "^GSPC"
    DOW_JONES = "^DJI"
    KOSPI = "^KS11"
    KOSDAQ = "^KQ11"
    NIKKEI_225 = "^N225"
    FTSE_100 = "^FTSE"
    DAX = "^GDAXI"
    CAC_40 = "^FCHI"
    EURO_STOXX_50 = "^STOXX50E"
    Shanghai = "^NSEI"
    Hang_Seng = "^HSI"
