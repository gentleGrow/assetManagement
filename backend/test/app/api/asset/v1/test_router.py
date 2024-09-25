from app.module.asset.enum import AccountType, InvestmentBankType

# class TestGetDummyAssetStock:
#     """
#     api: /api/v1/sample/assetstock
#     method: GET
#     """

#     async def test_not_found(
#         self,
#         client,
#         setup_asset,
#         setup_exchange_rate,
#         setup_realtime_stock_price,
#         setup_stock_daily,
#         setup_user,
#     ):
#         # Given
#         response = client.get("/api/v1/sample/assetstock?base_currency=won")

#         # When
#         response_data = response.json()

#         # Then
#         assert response.status_code == status.HTTP_404_NOT_FOUND
#         assert "다음의 주식 코드를 찾지 못 했습니다." in response_data["detail"]
#         not_found_stock_codes = response_data["detail"]["다음의 주식 코드를 찾지 못 했습니다."]

#         expected_not_found_stock_codes = ["UNKNOWN_CODE"]
#         assert not_found_stock_codes == expected_not_found_stock_codes


class TestGetBankAccounts:
    """
    api: /api/v1/bank-accounts
    method: GET
    """

    async def test_get_bank_accounts(self, client):
        # given
        response = client.get("/api/v1/bank-accounts")

        # when
        response_data = response.json()
        expected_investment_banks = [bank.value for bank in InvestmentBankType]
        expected_account_types = [account.value for account in AccountType]

        # then
        assert response_data["investment_bank_list"] == expected_investment_banks
        assert response_data["account_list"] == expected_account_types


class TestGetStockList:
    """
    api: /api/v1/stocks
    method: GET
    """

    async def test_get_stock_list(self, client, setup_stock):
        # Given
        setup_stock

        # When
        response = client.get("/api/v1/stocks")

        # Then
        response_data = response.json()

        expected_stocks = [
            {"name": "Apple Inc.", "code": "AAPL"},
            {"name": "Tesla Inc.", "code": "TSLA"},
            {"name": "삼성전자", "code": "005930"},
        ]

        assert response_data == expected_stocks
