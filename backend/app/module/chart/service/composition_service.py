from app.module.asset.enum import CurrencyType
from app.module.asset.model import Asset
from app.module.asset.services.exchange_rate_service import ExchangeRateService
from app.module.chart.constant import NONE_ACCOUNT


class CompositionService:
    @staticmethod
    def get_asset_stock_composition(
        assets: list[Asset], current_stock_price_map: dict[str, float], exchange_rate_map: dict[str, float]
    ) -> list[dict]:
        total_portfolio_value = 0.0
        stock_composition = {}

        for asset in assets:
            source_country = asset.asset_stock.stock.country.upper().strip()
            source_currency = CurrencyType[source_country]
            won_exchange_rate = ExchangeRateService.get_exchange_rate(
                source_currency, CurrencyType.KOREA, exchange_rate_map
            )

            stock_code = asset.asset_stock.stock.code
            stock_name = asset.asset_stock.stock.name
            num_shares = asset.asset_stock.quantity
            stock_price = won_exchange_rate * current_stock_price_map.get(stock_code, 0)
            stock_value = num_shares * stock_price

            if stock_code not in stock_composition:
                stock_composition[stock_code] = {
                    "name": stock_name,
                    "total_value": stock_value,
                    "total_shares": num_shares,
                }
            else:
                stock_composition[stock_code]["total_value"] += stock_value
                stock_composition[stock_code]["total_shares"] += num_shares

            total_portfolio_value += stock_value

        result = []
        for stock_data in stock_composition.values():
            proportion = (stock_data["total_value"] / total_portfolio_value) * 100 if total_portfolio_value > 0 else 0

            result.append(
                {"name": stock_data["name"], "percent_rate": proportion, "current_amount": stock_data["total_value"]}
            )

        return result

    @staticmethod
    def get_asset_stock_account(
        assets: list[Asset], current_stock_price_map: dict[str, float], exchange_rate_map: dict[str, float]
    ) -> list[dict]:
        total_portfolio_value = 0.0
        account_composition = {}

        for asset in assets:
            source_country = asset.asset_stock.stock.country.upper().strip()
            source_currency = CurrencyType[source_country]
            won_exchange_rate = ExchangeRateService.get_exchange_rate(
                source_currency, CurrencyType.KOREA, exchange_rate_map
            )

            stock_code = asset.asset_stock.stock.code
            account_type = asset.asset_stock.account_type

            num_shares = asset.asset_stock.quantity
            stock_price = won_exchange_rate * current_stock_price_map.get(stock_code, 0)
            stock_value = num_shares * stock_price

            if account_type not in account_composition:
                account_composition[account_type] = 0.0

            account_composition[account_type] += stock_value
            total_portfolio_value += stock_value

        result = []
        for account, account_value in account_composition.items():
            proportion = (account_value / total_portfolio_value) * 100 if total_portfolio_value > 0 else 0

            account_name = account.value if account else NONE_ACCOUNT
            result.append({"name": account_name, "percent_rate": proportion, "current_amount": account_value})
        return result
