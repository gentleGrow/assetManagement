from datetime import datetime, timedelta, timezone
from os import getenv
from typing import Any

from dotenv import load_dotenv
from fastapi import HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode

from app.module.auth.constant import JWT_ACCESS_TIME_MINUTE, JWT_REFRESH_TIME_MINUTE

load_dotenv()
JWT_SECRET_KEY = getenv("JWT_SECRET", None)
JWT_ALGORITHM = getenv("JWT_ALGORITHM", None)


class JWTBuilder:
    @staticmethod
    def generate_access_token(user_id: Any, social_id: Any) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_TIME_MINUTE)
        payload = {"exp": expire, "user": str(user_id), "sub": str(social_id)}
        return encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def generate_refresh_token(user_id: Any, social_id: Any) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_REFRESH_TIME_MINUTE)
        payload = {"exp": expire, "user": str(user_id), "sub": str(social_id)}
        return encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        try:
            return decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token이 만료되었습니다.")
        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 token입니다.")
