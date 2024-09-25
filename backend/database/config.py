import logging
from os import getenv

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from database.constant import MAX_OVERFLOW, POOL_SIZE
from database.enum import EnvironmentType

load_dotenv()


logging.basicConfig(
    filename="router_query.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

ENVIRONMENT = getenv("ENVIRONMENT", None)


if ENVIRONMENT == EnvironmentType.DEV:
    MYSQL_URL = getenv("LOCAL_MYSQL_URL", None)
    mysql_engine = create_async_engine(
        MYSQL_URL, pool_pre_ping=True, echo=False, pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW
    )
elif ENVIRONMENT == EnvironmentType.TEST:
    MYSQL_URL = getenv("TEST_DATABASE_URL", None)
    mysql_engine = create_async_engine(
        MYSQL_URL, pool_pre_ping=True, echo=False, pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW
    )
else:
    MYSQL_URL = getenv("MYSQL_URL", None)
    mysql_engine = create_async_engine(MYSQL_URL, pool_pre_ping=True, pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW)

mysql_session_factory = sessionmaker(bind=mysql_engine, class_=AsyncSession, expire_on_commit=False)
MySQLBase = declarative_base()
