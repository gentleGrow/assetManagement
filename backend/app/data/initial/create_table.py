from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from app.module.asset.model import (  # noqa > relationship purpose
    Asset,
    AssetField,
    Dividend,
    MarketIndexDaily,
    MarketIndexMinutely,
    MarketIndexMonthly,
    MarketIndexWeekly,
    Stock,
    StockDaily,
    StockMinutely,
    StockMonthly,
    StockWeekly,
)
from app.module.auth.model import User  # noqa > relationship purpose
from app.module.chart.model import InvestTip  # noqa > create table
from database.config import MYSQL_URL, MySQLBase

print("[create_tables] 테이블 생성을 시도 합니다.")


def main():
    if MYSQL_URL is not None:
        sync_mysql_url = MYSQL_URL.replace("mysql+aiomysql", "mysql+mysqlconnector")

        try:
            sync_engine = create_engine(sync_mysql_url)
            MySQLBase.metadata.create_all(sync_engine)
            print("[create_tables] 성공적으로 테이블을 생성하였습니다.")
        except SQLAlchemyError as e:
            print(f"[create_tables] SQLAlchemyError: {e}")
        except Exception as e:
            print(f"[create_tables] Unexpected error: {e}")
    else:
        print(f"[create_tables] MYSQL_URL가 정의 되어 있지 않습니다., {MYSQL_URL=}")


if __name__ == "__main__":
    main()
