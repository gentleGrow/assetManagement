from sqlalchemy import (
    JSON,
    BigInteger,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.common.mixin.timestamp import TimestampMixin
from app.module.asset.enum import AccountType, AssetType, InvestmentBankType, PurchaseCurrencyType
from database.config import MySQLBase


class AssetField(TimestampMixin, MySQLBase):
    __tablename__ = "asset_field"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False, unique=True)
    field_preference = Column(JSON, nullable=False, default=list)


class Dividend(TimestampMixin, MySQLBase):
    __tablename__ = "dividend"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    dividend = Column(Float, nullable=False, info={"description": "배당금"})
    stock_code = Column(String(255), ForeignKey("stock.code"), nullable=False)
    date = Column(Date, nullable=False, info={"description": "배당일자"})

    stock = relationship("Stock", back_populates="dividend")
    __table_args__ = (UniqueConstraint("stock_code", "date", name="uq_code_date"),)


class AssetStock(TimestampMixin, MySQLBase):
    __tablename__ = "asset_stock"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    account_type = Column(Enum(AccountType), nullable=True, info={"description": "계좌 종류"})
    investment_bank = Column(Enum(InvestmentBankType), nullable=True, info={"description": "증권사"})
    purchase_currency_type = Column(Enum(PurchaseCurrencyType), nullable=True, info={"description": "구매 통화"})
    purchase_date = Column(Date, nullable=False, info={"description": "구매일자"})
    purchase_price = Column(Float, nullable=True, info={"description": "매입가"})
    quantity = Column(Integer, nullable=False, info={"description": "구매수량"})

    stock_id = Column(BigInteger, ForeignKey("stock.id"), primary_key=True)
    asset_id = Column(BigInteger, ForeignKey("asset.id"), primary_key=True)
    asset = relationship("Asset", back_populates="asset_stock", uselist=False, overlaps="stock,asset", lazy="selectin")
    stock = relationship("Stock", back_populates="asset_stock", overlaps="asset,stock", lazy="selectin")


class Asset(TimestampMixin, MySQLBase):
    __tablename__ = "asset"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    asset_type = Column(Enum(AssetType), nullable=False, info={"description": "자산 종류"})

    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="asset")
    stock = relationship(
        "Stock", secondary="asset_stock", back_populates="asset", overlaps="asset_stock", lazy="selectin"
    )
    asset_stock = relationship("AssetStock", back_populates="asset", uselist=False, overlaps="stock", lazy="selectin")


class Stock(TimestampMixin, MySQLBase):
    __tablename__ = "stock"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(255), nullable=False, unique=True)
    country = Column(String(255), nullable=False)
    market_index = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)

    asset = relationship(
        "Asset", secondary="asset_stock", back_populates="stock", overlaps="asset_stock", lazy="selectin"
    )
    asset_stock = relationship("AssetStock", back_populates="stock", overlaps="asset", lazy="selectin")
    dividend = relationship("Dividend", back_populates="stock")


class StockMinutely(MySQLBase):
    __tablename__ = "stock_minutely"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(255), nullable=False)
    datetime = Column(DateTime, nullable=False)
    current_price = Column(Float, nullable=False)

    __table_args__ = (UniqueConstraint("code", "datetime", name="uq_code_name_datetime"),)


class StockDaily(MySQLBase):
    __tablename__ = "stock_daily"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    adj_close_price = Column(Float, nullable=False, info={"description": "Adjusted closing price of the stock"})
    close_price = Column(Float, nullable=False, info={"description": "Closing price of the stock"})
    code = Column(String(255), nullable=False)
    date = Column(Date, primary_key=True, nullable=False, info={"description": "stock closing day"})
    highest_price = Column(Float, nullable=False, info={"description": "Highest price of the stock"})
    lowest_price = Column(Float, nullable=False, info={"description": "Lowest price of the stock"})
    opening_price = Column(Float, nullable=False, info={"description": "Opening price of the stock"})
    trade_volume = Column(BigInteger, nullable=False, info={"description": "Volume of stock traded"})

    __table_args__ = (UniqueConstraint("code", "date", name="uq_code_date"), Index("idx_code_date", "code", "date"))


class StockWeekly(MySQLBase):
    __tablename__ = "stock_weekly"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    adj_close_price = Column(Float, nullable=False, info={"description": "Adjusted closing price of the stock"})
    close_price = Column(Float, nullable=False, info={"description": "Closing price of the stock"})
    code = Column(String(255), nullable=False)
    date = Column(Date, primary_key=True, nullable=False, info={"description": "stock closing week"})
    highest_price = Column(Float, nullable=False, info={"description": "Highest price of the stock"})
    lowest_price = Column(Float, nullable=False, info={"description": "Lowest price of the stock"})
    opening_price = Column(Float, nullable=False, info={"description": "Opening price of the stock"})
    trade_volume = Column(BigInteger, nullable=False, info={"description": "Volume of stock traded"})

    ___table_args__ = (UniqueConstraint("code", "date", name="uq_code_date"),)


class StockMonthly(MySQLBase):
    __tablename__ = "stock_monthly"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    adj_close_price = Column(Float, nullable=False, info={"description": "Adjusted closing price of the stock"})
    close_price = Column(Float, nullable=False, info={"description": "Closing price of the stock"})
    code = Column(String(255), nullable=False)
    date = Column(Date, primary_key=True, nullable=False, info={"description": "stock closing month"})
    highest_price = Column(Float, nullable=False, info={"description": "Highest price of the stock"})
    lowest_price = Column(Float, nullable=False, info={"description": "Lowest price of the stock"})
    opening_price = Column(Float, nullable=False, info={"description": "Opening price of the stock"})
    trade_volume = Column(BigInteger, nullable=False, info={"description": "Volume of stock traded"})

    ___table_args__ = (UniqueConstraint("code", "date", name="uq_code_date"),)


class MarketIndexMinutely(MySQLBase):
    __tablename__ = "market_index_minutely"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    datetime = Column(DateTime, nullable=False)
    current_price = Column(Float, nullable=False)

    __table_args__ = (UniqueConstraint("name", "datetime", name="uq_name_datetime"),)


class MarketIndexDaily(MySQLBase):
    __tablename__ = "market_index_daily"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    open_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    volume = Column(BigInteger, nullable=True)

    __table_args__ = (UniqueConstraint("name", "date", name="uq_name_date"),)


class MarketIndexWeekly(MySQLBase):
    __tablename__ = "market_index_weekly"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    open_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    volume = Column(BigInteger, nullable=False)

    __table_args__ = (UniqueConstraint("name", "date", name="uq_name_date"),)


class MarketIndexMonthly(MySQLBase):
    __tablename__ = "market_index_monthly"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    open_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    volume = Column(BigInteger, nullable=False)

    __table_args__ = (UniqueConstraint("name", "date", name="uq_name_date"),)
