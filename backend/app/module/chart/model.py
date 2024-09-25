from sqlalchemy import BigInteger, Column, String

from app.common.mixin.timestamp import TimestampMixin
from database.config import MySQLBase


class InvestTip(TimestampMixin, MySQLBase):
    __tablename__ = "invest_tip"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tip = Column(String(255), nullable=False)
