from app.module.asset.enum import TimeInterval
from app.module.asset.model import StockDaily, StockMonthly, StockWeekly
from app.module.asset.repository.stock_daily_repository import StockDailyRepository
from app.module.asset.repository.stock_monthly_repository import StockMonthlyRepository
from app.module.asset.repository.stock_weekly_repository import StockWeeklyRepository

STOCK_SCHEDULE_INTERVAL = "7d"
STOCK_TIME_INTERVAL = "1d"
STOCK_HISTORY_TIMERANGE_YEAR = 15
BATCH_SIZE = 100


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
