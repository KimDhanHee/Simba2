from api.crawler import *
from db.db import *
import pandas as pd


def main():
    db = Database()

    stocks = fetch_stocks()

    tickers = list(map(lambda stock: stock["symbol"], stocks))
    tickers = sorted(tickers)

    for idx, ticker in enumerate(tickers):
        print(f"======= {idx + 1} / {len(tickers)}. {ticker} =======")
        stock_df = pd.DataFrame(fetch_metrics(ticker))
        db.insert_quarterly_financial_report(stock_df)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
