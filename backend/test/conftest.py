import asyncio
from os import getenv

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.common.auth.security import verify_jwt_token
from app.module.asset.model import Stock, StockDaily, StockMonthly, StockWeekly  # noqa: F401 > relationship 설정시 필요합니다.
from app.module.auth.model import User  # noqa: F401 > relationship 설정시 필요합니다.
from database.config import MySQLBase
from database.dependency import get_test_redis_pool
from main import app

load_dotenv()


TEST_DATABASE_URL = getenv("TEST_DATABASE_URL", None)


test_engine = create_async_engine(TEST_DATABASE_URL, pool_pre_ping=True, poolclass=NullPool)
TestSessionLocal = sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def create_tables():
    async with test_engine.begin() as conn:
        await conn.run_sync(MySQLBase.metadata.create_all)


async def drop_tables():
    async with test_engine.begin() as conn:
        await conn.run_sync(MySQLBase.metadata.drop_all)


@pytest.fixture(scope="function")
async def session():
    async with TestSessionLocal() as test_session:
        await create_tables()
        yield test_session
        await test_session.rollback()
        await drop_tables()


@pytest.fixture(scope="function")
async def redis_client():
    redis = get_test_redis_pool()
    yield redis
    await redis.flushall()
    await redis.close()


def override_verify_jwt_token():
    return {"user": 999}


@pytest.fixture(scope="function")
def override_dependencies():
    app.dependency_overrides[verify_jwt_token] = override_verify_jwt_token
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c
