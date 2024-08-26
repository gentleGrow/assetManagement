from datetime import datetime

from pydantic import BaseModel

from app.module.auth.enum import ProviderEnum, UserRoleEnum


class User(BaseModel):
    id: int
    social_id: str
    provider: ProviderEnum
    role: UserRoleEnum
    nickname: str | None
    created_at: datetime
    deleted_at: datetime | None


class AccessToken(BaseModel):
    exp: int
    user: int
    sub: str


class TokenRequest(BaseModel):
    id_token: str


class NaverTokenRequest(BaseModel):
    access_token: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str
