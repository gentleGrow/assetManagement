from dataclasses import dataclass
from datetime import date


@dataclass
class StockAssetObject:
    id: int
    account_type: str | None
    buy_date: date
    current_price: float
    dividend: float
    highest_price: float | None
    investment_bank: str | None
    lowest_price: float | None
    opening_price: float | None
    profit_rate: float | None
    profit_amount: float | None
    purchase_amount: float | None
    purchase_price: float | None
    purchase_currency_type: str | None
    quantity: int
    stock_code: str
    stock_name: str
    stock_volume: int | None
