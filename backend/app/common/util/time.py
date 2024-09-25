import calendar
import time
from datetime import datetime
from zoneinfo import ZoneInfo


def get_now_datetime():
    seoul_tz = ZoneInfo("Asia/Seoul")
    return datetime.now(seoul_tz).replace(second=0, microsecond=0)


def start_timestamp(year: int, month: int) -> int:
    date = datetime(year, month, 1, 0, 0)
    return int(time.mktime(date.timetuple()))


def end_timestamp(year: int, month: int) -> int:
    last_day = calendar.monthrange(year, month)[1]
    date = datetime(year, month, last_day, 23, 59)
    return int(time.mktime(date.timetuple()))
