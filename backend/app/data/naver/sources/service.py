import asyncio

from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup

from app.module.asset.schema import StockInfo


async def fetch_stock_price(session: ClientSession, code: str) -> int:
    try:
        url = f"https://finance.naver.com/item/main.nhn?code={code}"
        async with session.get(url, timeout=ClientTimeout(total=2)) as response:
            response.raise_for_status()
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            today = soup.select_one("#chart_area > div.rate_info > div.today")

            if today is None:
                return 0

            no_today = today.select_one("p.no_today")
            if no_today:
                price_element = no_today.select_one("em.no_up .blind") or no_today.select_one("em.no_down .blind")
                if price_element:
                    price_text = price_element.get_text()
                    return int(price_text.replace(",", ""))
            else:
                price_text = today.select_one(".blind").get_text()
                return int(price_text.replace(",", ""))
    except Exception:
        return 0
    return 0


async def get_stock_prices(code_list: list[StockInfo]) -> list[tuple[str, int | Exception]]:
    async with ClientSession() as session:
        tasks = [fetch_stock_price(session, stockInfo.code) for stockInfo in code_list]
        prices = await asyncio.gather(*tasks, return_exceptions=True)
        return [(stockInfo.code, result) for stockInfo, result in zip(code_list, prices)]
