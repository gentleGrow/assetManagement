import asyncio

from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup

from app.module.asset.schema.stock_schema import StockInfo


async def fetch_stock_price(session: ClientSession, code: str) -> int:
    url = f"https://finance.naver.com/item/main.nhn?code={code}"
    timeout = ClientTimeout(total=2)

    try:
        async with session.get(url, timeout=timeout) as response:
            response.raise_for_status()
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            today = soup.select_one("#chart_area > div.rate_info > div")
            if today is None:
                return 0

            price_text = today.select_one(".blind").get_text()
            return int(price_text.replace(",", ""))
    except Exception as e:
        print(f"Error fetching stock price for {code}: {e}")
        return 0


async def get_stock_prices(code_list: list[StockInfo]) -> list[tuple[str, int | Exception]]:
    async with ClientSession() as session:
        tasks = [fetch_stock_price(session, stockInfo.code) for stockInfo in code_list]

        prices = await asyncio.gather(*tasks, return_exceptions=True)
        return [(stockInfo.code, result) for stockInfo, result in zip(code_list, prices)]
