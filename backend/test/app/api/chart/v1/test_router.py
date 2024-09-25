# from unittest.mock import patch

# import pytest
# from fastapi import status

# class TestGetTodayTip:
#     @pytest.mark.asyncio
#     async def test_tip_id_not_cached(self, client, mock_redis_repositories):
#         response = client.get(
#             "/api/chart/v1/tip",
#             headers={"Authorization": "Bearer testtoken"},
#         )
#         assert response.status_code == status.HTTP_404_NOT_FOUND
#         assert response.json()["detail"] == "오늘의 팁 id가 캐싱되어 있지 않습니다."

#     @pytest.mark.asyncio
#     async def test_tip_data_not_found(self, client, mock_redis_repositories):
#         with patch("app.module.chart.redis_repository.RedisTipRepository.get", return_value="1"):
#             response = client.get(
#                 "/api/chart/v1/tip",
#                 headers={"Authorization": "Bearer testtoken"},
#             )
#             assert response.status_code == status.HTTP_404_NOT_FOUND
#             assert response.json()["detail"] == "오늘의 팁 데이터가 존재하지 않습니다."


# [수정] aync 문제 발생, 추후 원인 파악
# class TestGetSummary:
#     @pytest.mark.asyncio
#     async def test_assets_length_zero(self, client):
#         response = client.get(
#             "/api/chart/v1/summary",
#             headers={"Authorization": "Bearer testtoken"},
#         )
#         assert response.status_code == status.HTTP_200_OK
#         assert response.json() == {
#             "today_review_rate": 0.0,
#             "total_asset_amount": 0,
#             "total_investment_amount": 0,
#             "profit_amount": 0,
#             "profit_rate": 0.0,
#         }
