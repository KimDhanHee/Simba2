import pymysql
from sqlalchemy import create_engine

from .config import *


class Database:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)

        if not hasattr(cls, '_init'):
            cls._init = True

            pymysql.install_as_MySQLdb()

            self.__engine = create_engine(
                f"mysql+pymysql://{DB_ID}:{DB_PW}@{HOSTNAME}:{PORT}/{DB_NAME_SIMBA}?charset=utf8"
            )

    def is_corp_saved(self, ticker, year, month) -> bool:
        sql = f"SELECT 1 FROM {TABLE_NAME_QUARTERLY_FINANCIAL_REPORT} " \
              f"WHERE ticker='{ticker}' year='{year}' and month='{month}'"
        rows = self.__engine.execute(sql).fetchall()
        return len(rows) > 0

    def insert_quarterly_financial_report(self, df):
        with self.__engine.connect():
            df.to_sql(
                name=TABLE_NAME_QUARTERLY_FINANCIAL_REPORT,
                con=self.__engine,
                if_exists='append',
                index=False
            )
