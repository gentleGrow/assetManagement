from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.repository.stock_daily_repository import StockDailyRepository


class TestStockDailyRepository:
    async def test_get_latest(self, session: AsyncSession, setup_stock_daily):
        # Given
        stock_codes = ["AAPL", "TSLA"]

        # When
        latest_stock_dailies = await StockDailyRepository.get_latest(session, stock_codes)

        # Then
        assert len(latest_stock_dailies) == 2

        aapl_stock_daily = next(sd for sd in latest_stock_dailies if sd.code == "AAPL")
        assert aapl_stock_daily.code == "AAPL"
        assert aapl_stock_daily.date == date(2024, 8, 14)

        tsla_stock_daily = next(sd for sd in latest_stock_dailies if sd.code == "TSLA")
        assert tsla_stock_daily.code == "TSLA"
        assert tsla_stock_daily.date == date(2024, 8, 14)

    async def test_get_stock_dailies_by_code_and_date(self, session: AsyncSession, setup_stock_daily) -> None:
        # Given
        setup_stock_daily

        stock_code_date_pairs = [
            ("AAPL", date(2024, 8, 13)),
            ("AAPL", date(2024, 8, 14)),
            ("TSLA", date(2024, 8, 13)),
            ("TSLA", date(2024, 8, 14)),
        ]

        # When
        stock_dailies = await StockDailyRepository.get_stock_dailies_by_code_and_date(session, stock_code_date_pairs)

        # Then
        assert stock_dailies[0].code == "AAPL"
        assert stock_dailies[0].date == date(2024, 8, 13)
        assert stock_dailies[0].adj_close_price == 150.0
        assert stock_dailies[0].close_price == 148.0

        assert stock_dailies[1].code == "AAPL"
        assert stock_dailies[1].date == date(2024, 8, 14)
        assert stock_dailies[1].adj_close_price == 151.0
        assert stock_dailies[1].close_price == 149.0

        assert stock_dailies[2].code == "TSLA"
        assert stock_dailies[2].date == date(2024, 8, 13)
        assert stock_dailies[2].adj_close_price == 720.0
        assert stock_dailies[2].close_price == 715.0

        assert stock_dailies[3].code == "TSLA"
        assert stock_dailies[3].date == date(2024, 8, 14)
        assert stock_dailies[3].adj_close_price == 725.0
        assert stock_dailies[3].close_price == 720.0
