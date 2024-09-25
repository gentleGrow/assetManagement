# from unittest.mock import patch

# import pytest
# from fastapi import status
# from fastapi.testclient import TestClient

# from app.module.auth.jwt import JWTBuilder
# from main import app

# client = TestClient(app)


# class TestNaverLogin:
#     @pytest.mark.asyncio
#     async def test_naver_login_no_id_token(self):
#         request_payload = {}

#         response = client.post("/api/auth/v1/naver", json=request_payload)

#         assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

#         response_data = response.json()

#         assert response_data["detail"][0]["msg"] == "Field required"
#         assert response_data["detail"][0]["type"] == "missing"

#     @pytest.mark.asyncio
#     @patch("app.api.auth.v1.router.Naver.verify_token")
#     async def test_naver_login_missing_sub(self, mock_naver_verify):
#         mock_naver_verify.return_value = {"response": {}}

#         request_payload = {"access_token": "fake_access_token"}
#         response = client.post("/api/auth/v1/naver", json=request_payload)

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         response_data = response.json()
#         assert response_data["detail"] == "access token에 유저 정보가 없습니다."

#     @pytest.mark.asyncio
#     @pytest.mark.asyncio
#     @patch("app.api.auth.v1.router.Naver.verify_token")
#     @patch("app.api.auth.v1.router.UserRepository.get_by_social_id")
#     @patch("app.api.auth.v1.router.UserRepository.create")
#     async def test_naver_login_user_creation(
#         self, mock_create_user, mock_get_user, mock_naver_verify, user_instance, mock_redis_repositories
#     ):
#         mock_naver_verify.return_value = {"response": {"id": "naver_social_id"}}
#         mock_get_user.return_value = None
#         mock_create_user.return_value = user_instance

#         request_payload = {"access_token": "fake_access_token"}

#         response = client.post("/api/auth/v1/naver", json=request_payload)

#         assert response.status_code == status.HTTP_200_OK
#         response_data = response.json()

#         assert "access_token" in response_data
#         assert "refresh_token" in response_data

#         assert JWTBuilder.decode_token(response_data["access_token"])["user"] == "1"
#         assert JWTBuilder.decode_token(response_data["refresh_token"])["user"] == "1"


# class TestKakaoLogin:
#     @pytest.mark.asyncio
#     async def test_kakao_login_no_id_token(self):
#         request_payload = {}

#         response = client.post("/api/auth/v1/kakao", json=request_payload)

#         assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

#         response_data = response.json()

#         assert response_data["detail"][0]["msg"] == "Field required"
#         assert response_data["detail"][0]["type"] == "missing"

#     @pytest.mark.asyncio
#     @patch("app.api.auth.v1.router.Kakao.verify_token")
#     async def test_kakao_login_missing_sub(self, mock_kakao_verify):
#         mock_kakao_verify.return_value = {}

#         request_payload = {"id_token": "fake_id_token"}
#         response = client.post("/api/auth/v1/kakao", json=request_payload)

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         response_data = response.json()
#         assert response_data["detail"] == "id token에 유저 정보가 없습니다."

#     @pytest.mark.asyncio
#     @patch("app.api.auth.v1.router.Kakao.verify_token")
#     @patch("app.api.auth.v1.router.UserRepository.get_by_social_id")
#     @patch("app.api.auth.v1.router.UserRepository.create")
#     async def test_google_login_user_creation(
#         self, mock_create_user, mock_get_user, mock_kakao_verify, user_instance, mock_redis_repositories
#     ):
#         mock_kakao_verify.return_value = {"sub": "kakao_social_id"}
#         mock_get_user.return_value = None
#         mock_create_user.return_value = user_instance

#         request_payload = {"id_token": "fake_id_token"}

#         response = client.post("/api/auth/v1/kakao", json=request_payload)

#         assert response.status_code == status.HTTP_200_OK
#         response_data = response.json()

#         assert "access_token" in response_data
#         assert "refresh_token" in response_data

#         assert JWTBuilder.decode_token(response_data["access_token"])["user"] == "1"
#         assert JWTBuilder.decode_token(response_data["refresh_token"])["user"] == "1"


# class TestGoogleLogin:
#     @pytest.mark.asyncio
#     async def test_google_login_no_id_token(self):
#         request_payload = {}

#         response = client.post("/api/auth/v1/google", json=request_payload)

#         assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

#         response_data = response.json()

#         assert response_data["detail"][0]["msg"] == "Field required"
#         assert response_data["detail"][0]["type"] == "missing"

#     @pytest.mark.asyncio
#     @patch("app.api.auth.v1.router.Google.verify_token")
#     async def test_google_login_missing_sub(self, mock_google_verify):
#         mock_google_verify.return_value = {}

#         request_payload = {"id_token": "fake_id_token"}
#         response = client.post("/api/auth/v1/google", json=request_payload)

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         response_data = response.json()
#         assert response_data["detail"] == "id token에 유저 정보가 없습니다."

#     @pytest.mark.asyncio
#     @patch("app.api.auth.v1.router.Google.verify_token")
#     @patch("app.api.auth.v1.router.UserRepository.get_by_social_id")
#     @patch("app.api.auth.v1.router.UserRepository.create")
#     async def test_google_login_user_creation(
#         self, mock_create_user, mock_get_user, mock_google_verify, user_instance, mock_redis_repositories
#     ):
#         mock_google_verify.return_value = {"sub": "google_social_id"}
#         mock_get_user.return_value = None
#         mock_create_user.return_value = user_instance

#         request_payload = {"id_token": "fake_id_token"}

#         response = client.post("/api/auth/v1/google", json=request_payload)

#         assert response.status_code == status.HTTP_200_OK
#         response_data = response.json()

#         assert "access_token" in response_data
#         assert "refresh_token" in response_data

#         assert JWTBuilder.decode_token(response_data["access_token"])["user"] == "1"
#         assert JWTBuilder.decode_token(response_data["refresh_token"])["user"] == "1"


# class TestRefreshAccessToken:
#     @pytest.mark.asyncio
#     @patch("app.api.auth.v1.router.JWTBuilder.decode_token")
#     async def test_refresh_access_token_social_id_none(self, mock_decode_token):
#         mock_decode_token.return_value = {"user": "1", "sub": None}

#         request_payload = {"refresh_token": "fake_refresh_token"}

#         response = client.post("/api/auth/v1/refresh", json=request_payload)

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#         response_data = response.json()
#         assert response_data["detail"] == "refresh token안에 유저 정보가 들어있지 않습니다."

#     @pytest.mark.asyncio
#     @patch("app.api.auth.v1.router.JWTBuilder.decode_token")
#     @patch("app.api.auth.v1.router.RedisSessionRepository.get")
#     async def test_refresh_access_token_stored_token_none(self, mock_redis_get, mock_decode_token):
#         mock_decode_token.return_value = {"user": "1", "sub": "social_id_value"}

#         mock_redis_get.return_value = None

#         request_payload = {"refresh_token": "fake_refresh_token"}

#         response = client.post("/api/auth/v1/refresh", json=request_payload)

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#         response_data = response.json()
#         assert response_data["detail"] == "서버에 저장된 refresh token이 없습니다."

#     @pytest.mark.asyncio
#     @patch("app.api.auth.v1.router.JWTBuilder.decode_token")
#     @patch("app.api.auth.v1.router.RedisSessionRepository.get")
#     async def test_refresh_access_token_stored_token_mismatch(self, mock_redis_get, mock_decode_token):
#         mock_decode_token.return_value = {"user": "1", "sub": "social_id_value"}

#         mock_redis_get.return_value = "different_stored_refresh_token"

#         request_payload = {"refresh_token": "fake_refresh_token"}

#         response = client.post("/api/auth/v1/refresh", json=request_payload)

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#         response_data = response.json()
#         assert response_data["detail"] == "서버에 저장된 refresh token과 다른 refresh token을 반환하였습니다."
