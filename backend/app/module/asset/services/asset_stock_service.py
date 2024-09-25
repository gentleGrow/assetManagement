from datetime import date, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.enum import AssetType, CurrencyType, PurchaseCurrencyType, StockAsset
from app.module.asset.model import Asset, AssetStock, StockDaily
from app.module.asset.repository.asset_field_repository import AssetFieldRepository
from app.module.asset.repository.asset_repository import AssetRepository
from app.module.asset.schema import AssetStockPostRequest
from app.module.asset.services.exchange_rate_service import ExchangeRateService


class AssetStockService:
    @staticmethod
    async def save_asset_stock_by_post(
        session: AsyncSession, request_data: AssetStockPostRequest, stock_id: int, user_id: int
    ) -> None:
        result = []

        new_asset = Asset(
            asset_type=AssetType.STOCK,
            user_id=user_id,
            asset_stock=AssetStock(
                account_type=request_data.account_type,
                investment_bank=request_data.investment_bank,
                purchase_currency_type=request_data.purchase_currency_type,
                purchase_date=request_data.buy_date,
                purchase_price=request_data.purchase_price,
                quantity=request_data.quantity,
                stock_id=stock_id,
            ),
        )
        result.append(new_asset)

        await AssetRepository.save_assets(session, result)

    @staticmethod
    def get_total_asset_amount_minute(
        assets: list[Asset],
        stock_interval_date_price_map: dict[str, float],
        exchange_rate_map: dict[str, float],
        current_datetime: datetime,
    ) -> float:
        result = 0.0

        for asset in assets:
            current_price = stock_interval_date_price_map.get(f"{asset.asset_stock.stock.code}_{current_datetime}")

            if current_price is None:
                continue
            source_country = asset.asset_stock.stock.country.upper().strip()
            source_currency = CurrencyType[source_country]

            won_exchange_rate = ExchangeRateService.get_exchange_rate(
                source_currency, CurrencyType.KOREA, exchange_rate_map
            )
            current_price *= won_exchange_rate
            result += current_price * asset.asset_stock.quantity
        return result

    @staticmethod
    def get_total_asset_amount(
        assets: list[Asset],
        current_stock_price_map: dict[str, float],
        exchange_rate_map: dict[str, float],
    ) -> float:
        result = 0.0

        for asset in assets:
            result += (
                current_stock_price_map.get(asset.asset_stock.stock.code)
                * asset.asset_stock.quantity
                * ExchangeRateService.get_won_exchange_rate(asset, exchange_rate_map)
            )
        return result

    @staticmethod
    async def get_stock_assets(
        session: AsyncSession,
        user_id: int,
        assets: list[Asset],
        stock_daily_map: dict[tuple[str, date], StockDaily],
        current_stock_price_map: dict[str, float],
        dividend_map: dict[str, float],
        exchange_rate_map: dict[str, float],
    ) -> list[dict]:
        asset_field = await AssetFieldRepository.get(session, user_id)
        stock_assets = []

        for asset in assets:
            apply_exchange_rate: float = (
                ExchangeRateService.get_dollar_exchange_rate(asset, exchange_rate_map)
                if asset.asset_stock.purchase_currency_type == PurchaseCurrencyType.USA
                else ExchangeRateService.get_won_exchange_rate(asset, exchange_rate_map)
            )

            stock_daily = stock_daily_map.get((asset.asset_stock.stock.code, asset.asset_stock.purchase_date), None)
            if stock_daily is None:
                continue

            purchase_price = (
                asset.asset_stock.purchase_price if asset.asset_stock.purchase_price else stock_daily.adj_close_price
            )

            stock_asset_data = {
                StockAsset.ID.value: asset.id,
                StockAsset.ACCOUNT_TYPE.value: asset.asset_stock.account_type or None,
                StockAsset.BUY_DATE.value: asset.asset_stock.purchase_date,
                StockAsset.CURRENT_PRICE.value: (
                    current_stock_price_map.get(asset.asset_stock.stock.code, 0.0) * apply_exchange_rate
                ),
                StockAsset.DIVIDEND.value: (
                    dividend_map.get(asset.asset_stock.stock.code, 0.0)
                    * asset.asset_stock.quantity
                    * apply_exchange_rate
                ),
                StockAsset.HIGHEST_PRICE.value: (stock_daily.highest_price * apply_exchange_rate)
                if stock_daily.highest_price
                else None,
                StockAsset.INVESTMENT_BANK.value: asset.asset_stock.investment_bank or None,
                StockAsset.LOWEST_PRICE.value: (stock_daily.lowest_price * apply_exchange_rate)
                if stock_daily.lowest_price
                else None,
                StockAsset.OPENING_PRICE.value: (stock_daily.opening_price * apply_exchange_rate)
                if stock_daily.opening_price
                else None,
                StockAsset.PROFIT_RATE.value: (
                    (
                        current_stock_price_map.get(asset.asset_stock.stock.code, 0.0) * apply_exchange_rate
                        - purchase_price
                    )
                    / purchase_price
                    * 100
                )
                if purchase_price
                else None,
                StockAsset.PROFIT_AMOUNT.value: (
                    (
                        current_stock_price_map.get(asset.asset_stock.stock.code, 0.0) * apply_exchange_rate
                        - purchase_price
                    )
                    * asset.asset_stock.quantity
                )
                if purchase_price
                else None,
                StockAsset.PURCHASE_AMOUNT.value: (asset.asset_stock.purchase_price * asset.asset_stock.quantity)
                if asset.asset_stock.purchase_price
                else None,
                StockAsset.PURCHASE_PRICE.value: asset.asset_stock.purchase_price or None,
                StockAsset.PURCHASE_CURRENCY_TYPE.value: asset.asset_stock.purchase_currency_type or None,
                StockAsset.QUANTITY.value: asset.asset_stock.quantity,
                StockAsset.STOCK_CODE.value: asset.asset_stock.stock.code,
                StockAsset.STOCK_NAME.value: asset.asset_stock.stock.name,
                StockAsset.STOCK_VOLUME.value: stock_daily.trade_volume if stock_daily.trade_volume else None,
            }

            stock_asset_data_filter = {
                field: value for field, value in stock_asset_data.items() if field in asset_field.field_preference
            }

            stock_assets.append(stock_asset_data_filter)

        return stock_assets

    @staticmethod
    def get_total_investment_amount(
        assets: list[Asset],
        stock_daily_map: dict[tuple[str, date], StockDaily],
        exchange_rate_map: dict[str, float],
    ) -> float:
        total_invest_amount = 0.0

        for asset in assets:
            stock_daily = stock_daily_map.get((asset.asset_stock.stock.code, asset.asset_stock.purchase_date), None)
            if stock_daily is None:
                continue

            invest_price = (
                asset.asset_stock.purchase_price * ExchangeRateService.get_won_exchange_rate(asset, exchange_rate_map)
                if asset.asset_stock.purchase_currency_type == PurchaseCurrencyType.USA
                and asset.asset_stock.purchase_price
                else asset.asset_stock.purchase_price
                if asset.asset_stock.purchase_price
                else stock_daily.adj_close_price * ExchangeRateService.get_won_exchange_rate(asset, exchange_rate_map)
            )

            total_invest_amount += invest_price * asset.asset_stock.quantity

        return total_invest_amount
