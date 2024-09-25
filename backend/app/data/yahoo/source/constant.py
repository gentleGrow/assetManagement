from app.module.asset.enum import TimeInterval
from app.module.asset.model import (
    MarketIndexDaily,
    MarketIndexMonthly,
    MarketIndexWeekly,
    StockDaily,
    StockMonthly,
    StockWeekly,
)
from app.module.asset.repository.market_index_daily_repository import MarketIndexDailyRepository
from app.module.asset.repository.market_index_monthly_repository import MarketIndexMonthlyRepository
from app.module.asset.repository.market_index_weekly_repository import MarketIndexWeeklyRepository
from app.module.asset.repository.stock_daily_repository import StockDailyRepository
from app.module.asset.repository.stock_monthly_repository import StockMonthlyRepository
from app.module.asset.repository.stock_weekly_repository import StockWeeklyRepository

STOCK_SCHEDULE_INTERVAL = "7d"
STOCK_TIME_INTERVAL = "1d"
STOCK_HISTORY_TIMERANGE_YEAR = 15
BATCH_SIZE = 100
REALTIME_STOCK_LIST = 200


TIME_INTERVAL_MODEL_REPO_MAP = {
    TimeInterval.DAY: StockDaily,
    TimeInterval.WEEK: StockWeekly,
    TimeInterval.MONTH: StockMonthly,
}

TIME_INTERVAL_REPOSITORY_MAP = {
    TimeInterval.DAY: StockDailyRepository,
    TimeInterval.WEEK: StockWeeklyRepository,
    TimeInterval.MONTH: StockMonthlyRepository,
}


MARKET_INDEX_TIME_INTERVALS = [
    (TimeInterval.DAY, MarketIndexDaily, MarketIndexDailyRepository),
    (TimeInterval.WEEK, MarketIndexWeekly, MarketIndexWeeklyRepository),
    (TimeInterval.MONTH, MarketIndexMonthly, MarketIndexMonthlyRepository),
]
