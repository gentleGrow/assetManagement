from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ProviderEnum(str, Enum):
    google = "google"
    kakao = "kakao"
    naver = "naver"


class UserRoleEnum(str, Enum):
    admin = "admin"
    user = "user"


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    social_id: str
    provider: ProviderEnum
    role: UserRoleEnum | None
    nickname: str | None
    created_at: datetime
    deleted_at: datetime | None

    # [정보] Config을 통해서 DB 데이터의 직렬화/비직렬화를 설정합니다. 이를 통해 직접 db에서 endpoint까지 데이터 변환 과정없이 전달이 가능합니다.
    class Config:
        from_attributes = True


class TokenRequest(BaseModel):
    access_token: str = Field(..., description="client에게 전달 받은 구글 access token입니다.")
    refresh_token: str = Field(..., description="client에게 전달 받은 구글 refresh token입니다.")
