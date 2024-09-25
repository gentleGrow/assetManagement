from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.repository.stock_repository import StockRepository


async def test_get_all_stocks(session: AsyncSession, setup_stock):
    # Given
    setup_stock

    # When
    stocks = await StockRepository.get_all(session)

    # Then
    assert stocks[0].code == "AAPL"
    assert stocks[0].name == "Apple Inc."
    assert stocks[1].code == "TSLA"
    assert stocks[1].name == "Tesla Inc."
