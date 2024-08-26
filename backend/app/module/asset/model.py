from sqlalchemy import BigInteger, Column, Date, Enum, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.common.mixin.timestamp import TimestampMixin
from app.module.asset.enum import AccountType, AssetType, InvestmentBankType, PurchaseCurrencyType
from database.config import MySQLBase


class Dividend(TimestampMixin, MySQLBase):
    __tablename__ = "dividend"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    dividend = Column(Float, nullable=False, info={"description": "배당금"})
    stock_code = Column(String(255), ForeignKey("stock.code"), nullable=False, unique=True)

    stock = relationship("Stock", back_populates="dividend")


class AssetStock(TimestampMixin, MySQLBase):
    __tablename__ = "asset_stock"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    account_type = Column(Enum(AccountType), nullable=False, info={"description": "계좌 종류"})
    investment_bank = Column(Enum(InvestmentBankType), nullable=False, info={"description": "증권사"})
    purchase_currency_type = Column(Enum(PurchaseCurrencyType), nullable=False, info={"description": "구매 통화"})
    purchase_date = Column(Date, nullable=False, info={"description": "구매일자"})
    purchase_price = Column(Float, nullable=True, info={"description": "매입가"})
    quantity = Column(Integer, nullable=False)

    stock_id = Column(BigInteger, ForeignKey("stock.id"), primary_key=True)
    asset_id = Column(BigInteger, ForeignKey("asset.id"), primary_key=True)
    asset = relationship("Asset", back_populates="asset_stock", uselist=False, overlaps="stock,asset")
    stock = relationship("Stock", back_populates="asset_stock", overlaps="asset,stock")


class Asset(TimestampMixin, MySQLBase):
    __tablename__ = "asset"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    asset_type = Column(Enum(AssetType), nullable=False, info={"description": "자산 종류"})

    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="asset")
    stock = relationship("Stock", secondary="asset_stock", back_populates="asset", overlaps="asset_stock")
    asset_stock = relationship("AssetStock", back_populates="asset", uselist=False, overlaps="stock")


class Stock(TimestampMixin, MySQLBase):
    __tablename__ = "stock"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(255), nullable=False, unique=True)
    country = Column(String(255), nullable=False)
    market_index = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)

    asset = relationship("Asset", secondary="asset_stock", back_populates="stock", overlaps="asset_stock")
    asset_stock = relationship("AssetStock", back_populates="stock", overlaps="asset")
    dividend = relationship("Dividend", back_populates="stock")


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

    __table_args__ = (UniqueConstraint("code", "date", name="uq_code_date"),)


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
