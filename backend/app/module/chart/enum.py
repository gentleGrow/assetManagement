from datetime import timedelta
from enum import StrEnum


class EstimateDividendType(StrEnum):
    EVERY = "every"
    TYPE = "type"


class CompositionType(StrEnum):
    COMPOSITION = "composition"
    ACCOUNT = "account"


class IntervalType(StrEnum):
    FIVEDAY = "5day"
    ONEMONTH = "1month"
    THREEMONTH = "3month"
    SIXMONTH = "6month"
    ONEYEAR = "1year"

    def get_timedelta(self) -> timedelta:
        if self == IntervalType.FIVEDAY:
            return timedelta(hours=5 * 24)
        elif self == IntervalType.ONEMONTH:
            return timedelta(days=30)
        elif self == IntervalType.THREEMONTH:
            return timedelta(days=90)
        elif self == IntervalType.SIXMONTH:
            return timedelta(days=180)
        elif self == IntervalType.ONEYEAR:
            return timedelta(days=360)
        return timedelta(days=30)

    def get_interval(self) -> int:
        if self == IntervalType.FIVEDAY:
            return 30
        elif self == IntervalType.ONEMONTH:
            return 1
        elif self == IntervalType.THREEMONTH:
            return 1
        elif self == IntervalType.SIXMONTH:
            return 1
        elif self == IntervalType.ONEYEAR:
            return 1
        return 1
