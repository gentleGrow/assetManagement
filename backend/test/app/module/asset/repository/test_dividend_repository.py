from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.repository.dividend_repository import DividendRepository


class TestDividendRepository:
    async def test_get_dividends_recent(self, session: AsyncSession, setup_dividend):
        # Given
        stock_codes = ["AAPL", "TSLA"]

        # When
        recent_dividends = await DividendRepository.get_dividends_recent(session, stock_codes)

        # Then
        assert len(recent_dividends) == 2

        dividend_aapl = next(dividend for dividend in recent_dividends if dividend.stock_code == "AAPL")
        assert dividend_aapl.stock_code == "AAPL"
        assert dividend_aapl.date == date(2024, 8, 14)

        dividend_tsla = next(dividend for dividend in recent_dividends if dividend.stock_code == "TSLA")
        assert dividend_tsla.stock_code == "TSLA"
        assert dividend_tsla.date == date(2024, 8, 14)
