from api.crawler import *
from db.db import *


def main():
    db = Database()

    stocks = fetch_stocks()

    tickers = list(map(lambda stock: stock["symbol"], stocks))
    tickers = sorted(tickers)

    for idx, ticker in enumerate(tickers):
        print(f"======= {idx + 1} / {len(tickers)}. {ticker} =======")

        recent_df = pd.DataFrame(fetch_metrics(ticker))
        last_df = db.fetch_ticker_financial_report(ticker, None, None)
        if len(last_df) > 0:
            try:
                new_df = pd.merge(
                    recent_df, last_df, how='outer', indicator=True
                ).query(
                    '_merge == "left_only"'
                ).drop(columns=['_merge'])

                if len(new_df) > 0:
                    db.insert_quarterly_financial_report(new_df)
            except Exception as e:
                print(e)
        else:
            db.insert_quarterly_financial_report(recent_df)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
