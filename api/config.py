API_KEY = "e558vSI8LyRrCGv5TqWJtFTAcMDoVD7c"

FETCH_STOCKS_URL = (
    f"https://financialmodelingprep.com/api/v3/stock-screener?apikey={API_KEY}&"
    f"exchange=nyse,nasdaq&isEtf=false&isFund=false&limit=10000"
)

# gross profit, earningspersharebasic
FETCH_INCOME_URL = f"https://financialmodelingprep.com/api/v3/income-statement/%s?period=quarter&limit=100&apikey={API_KEY}"
# totalAssets
FETCH_BALANCE_URL = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/%s?period=quarter&limit=100&apikey={API_KEY}"
# priceToSalesRatio
FETCH_RATIO_URL = f"https://financialmodelingprep.com/api/v3/ratios/%s?period=quarter&limit=100&apikey={API_KEY}"
# grossProfitGrowth, ebitgrowth
FETCH_GROWTH_URL = f"https://financialmodelingprep.com/api/v3/financial-growth/%s?period=quarter&limit=100&apikey={API_KEY}"
