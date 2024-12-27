import pandas as pd
import pymysql
from pandas import DataFrame
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

    def fetch_ticker_financial_report(self, ticker, from_date, to_date) -> DataFrame:
        sql = f"SELECT * FROM {TABLE_NAME_QUARTERLY_FINANCIAL_REPORT} WHERE symbol='{ticker}'"
        if from_date is not None and to_date is not None:
            sql = (f"SELECT * FROM {TABLE_NAME_QUARTERLY_FINANCIAL_REPORT} WHERE symbol='{ticker}' and "
                   f"date BETWEEN '{from_date}' and '{to_date}'")
        return pd.read_sql(sql, con=self.__engine)

    def insert_quarterly_financial_report(self, df):
        with self.__engine.connect():
            df.to_sql(
                name=TABLE_NAME_QUARTERLY_FINANCIAL_REPORT,
                con=self.__engine,
                if_exists='append',
                index=False
            )
