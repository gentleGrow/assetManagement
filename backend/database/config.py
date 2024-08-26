import logging
from os import getenv

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from database.enum import EnvironmentType

load_dotenv()


logging.basicConfig(
    filename="router_query.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.setLevel(logging.INFO)

ENVIRONMENT = getenv("ENVIRONMENT", None)

if ENVIRONMENT == EnvironmentType.DEV:
    MYSQL_URL = getenv("LOCAL_MYSQL_URL", None)
    mysql_engine = create_async_engine(MYSQL_URL, pool_pre_ping=True, echo=False)
else:
    MYSQL_URL = getenv("MYSQL_URL", None)
    mysql_engine = create_async_engine(MYSQL_URL, pool_pre_ping=True, echo=False)

mysql_session_factory = sessionmaker(bind=mysql_engine, class_=AsyncSession, expire_on_commit=False)
MySQLBase = declarative_base()
