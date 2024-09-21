import pytest
from fastapi import status
from app.module.asset.enum import AccountType, InvestmentBankType

class TestGetBankAccounts:
    """
    api: /api/v1/bank-accounts
    """
    async def test_get_bank_accounts(self, client):
        #given
        response = client.get("/api/v1/bank-accounts")
        
        #when
        response_data = response.json()
        expected_investment_banks = [bank.value for bank in InvestmentBankType]
        expected_account_types = [account.value for account in AccountType]
        
        #then
        assert response_data["investment_bank_list"] == expected_investment_banks
        assert response_data["account_list"] == expected_account_types





# class TestCreateAssets:
#     """
#     api: /api/v1/assetstock
#     method: POST
#     """
#     @pytest.mark.asyncio
#     async def test_create_assets_with_id_error(self, client, transaction_data_with_invalid_id):
#         response = client.post(
#             "/api/v1/assetstock",
#             json=transaction_data_with_invalid_id,
#             headers={"Authorization": "Bearer testtoken"},
#         )
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.json()["detail"] == "주식 자산 데이터 안에 id 값이 없어야 합니다."

#     @pytest.mark.asyncio
#     async def test_create_assets_stock_not_found(self, client, transaction_data_with_wrong_stock_code):
#         response = client.post(
#             "/api/v1/assetstock",
#             json=transaction_data_with_wrong_stock_code,
#             headers={"Authorization": "Bearer testtoken"},
#         )
#         assert response.status_code == status.HTTP_404_NOT_FOUND
#         assert response.json()["detail"] == "종목 코드 UNKNOWN_CODE에 해당하는 주식을 찾을 수 없습니다."


# class TestUpdateAssets:
#     """
#     api: /api/v1/assetstock
#     method: PUT
#     """
#     @pytest.mark.asyncio
#     async def test_update_assets_id_not_found(self, client, transaction_data_with_invalid_id):
#         response = client.put(
#             "/api/v1/assetstock",
#             json=transaction_data_with_invalid_id,
#             headers={"Authorization": "Bearer testtoken"},
#         )
#         assert response.status_code == status.HTTP_404_NOT_FOUND
#         assert response.json()["detail"] == "Asset ID 1234를 찾을 수 없습니다."

#     @pytest.mark.asyncio
#     async def test_update_assets_stock_not_found(self, client, transaction_data_with_wrong_stock_code):
#         transaction_data_with_wrong_stock_code[0]["id"] = 999
#         response = client.put(
#             "/api/v1/assetstock",
#             json=transaction_data_with_wrong_stock_code,
#             headers={"Authorization": "Bearer testtoken"},
#         )
#         assert response.status_code == status.HTTP_404_NOT_FOUND
#         assert response.json()["detail"] == "종목 코드 UNKNOWN_CODE에 해당하는 주식을 찾을 수 없습니다."


# class TestDeleteAsset:
#     """
#     api: /api/v1/assetstock
#     method: DELETE
#     """
#     @pytest.mark.asyncio
#     async def test_delete_asset_id_not_found(self, client):
#         response = client.delete(
#             "/api/v1/assetstock/1234",
#             headers={"Authorization": "Bearer testtoken"},
#         )
#         assert response.status_code == status.HTTP_404_NOT_FOUND
#         assert response.json()["detail"] == "Asset ID 1234를 찾을 수 없습니다."


# class TestGetAssets:
#     """
#     api: /api/v1/assetstock
#     method: GET
#     """
#     @pytest.mark.asyncio
#     async def test_get_assets_success(self, client):
#         response = client.get(
#             "/api/v1/assetstock",
#             headers={"Authorization": "Bearer testtoken"},
#         )
#         assert response.status_code == status.HTTP_200_OK


