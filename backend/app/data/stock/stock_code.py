import asyncio

from app.data.common.service import get_all_stock_code_list
from app.module.asset.model import Stock  # noqa: F401 > relationship 설정시 필요합니다.
from app.module.asset.repository.stock_repository import StockRepository
from app.module.asset.schema import StockInfo
from app.module.auth.model import User  # noqa: F401 > relationship 설정시 필요합니다.
from database.dependency import get_mysql_session


async def main():
    print("주식 코드 저장을 시작합니다.")
    async with get_mysql_session() as session:
        stock_list: list[StockInfo] = get_all_stock_code_list()
        stock_code_list = []

        for stock_info in stock_list:
            stock = Stock(
                code=stock_info.code,
                name=stock_info.name,
                market_index=stock_info.market_index,
                country=stock_info.country,
            )

            stock_code_list.append(stock)

        try:
            await StockRepository.bulk_upsert(session, stock_code_list)
        except Exception as e:
            print(f"{e=}")

    print("주식 코드 저장을 마칩니다.")


if __name__ == "__main__":
    asyncio.run(main())
