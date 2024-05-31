import json
from datetime import datetime
from urllib.request import urlopen

from .config import *


def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


def fetch_stocks():
    return get_jsonparsed_data(FETCH_STOCKS_URL)


def fetch_metrics(ticker):
    incomes = get_jsonparsed_data(FETCH_INCOME_URL % ticker)
    balances = get_jsonparsed_data(FETCH_BALANCE_URL % ticker)
    ratios = get_jsonparsed_data(FETCH_RATIO_URL % ticker)
    growths = get_jsonparsed_data(FETCH_GROWTH_URL % ticker)

    results = []

    size = min(len(incomes), len(balances), len(ratios), len(growths))

    for i in range(size):
        income = incomes[i]
        balance = balances[i]
        ratio = ratios[i]
        growth = growths[i]

        date = datetime.strptime(income["fillingDate"], "%Y-%m-%d")

        results.append(build_key_metrics(date, income, balance, ratio, growth))

    return results


def build_key_metrics(date, income, balance, ratio, growth):
    grossProfit = fetch_metric("grossProfit", income)
    totalAssets = fetch_metric("totalAssets", balance)

    return {
        "date": date,
        "year": date.year,
        "month": date.month,
        "period": income["period"],
        "symbol": income["symbol"],
        "revenue": fetch_metric("revenue", income),
        "gross_profit": grossProfit,
        # 매출 총 이익률 (매출 - 매출 원가) / 매출 -> 영업 효율 척도
        "gross_profit_ratio": fetch_metric("grossProfitRatio", income),
        # earnings before interest, taxes, depreciation and amortization
        # 순이익 + 감가상각비 (유 & 무형) + 세금 + 이자
        # 기업이 건강한지를 보여주는 지표
        "ebitda": fetch_metric("ebitda", income),
        # ev / ebitda
        "ebitda_ratio": fetch_metric("ebitdaratio", income),
        "operating_income": fetch_metric("operatingIncome", income),
        # 순이익
        "net_income": fetch_metric("netIncome", income),
        "net_income_ratio": fetch_metric("netIncomeRatio", income),
        "eps": fetch_metric("eps", income),
        "eps_diluted": fetch_metric("epsdiluted", income),
        "assets": totalAssets,
        "equity": fetch_metric("totalEquity", balance),
        "debt": fetch_metric("totalDebt", balance),
        "net_debt": fetch_metric("netDebt", balance),
        "gp_a": grossProfit / totalAssets if totalAssets != 0 else 0,
        # 유동 비율 : 유동 자산 / 유동 부채. 높을수록 안전
        "current_ratio": fetch_metric("currentRatio", ratio),
        # 당좌 비율 : 당좌 자산 / 유동 부채.
        "quick_ratio": fetch_metric("quickRatio", ratio),
        "cash_ratio": fetch_metric("cashRatio", ratio),
        "operating_profit_margin": fetch_metric("operatingProfitMargin", ratio),
        # return on assets. 총자산수익률
        "roa": fetch_metric("returnOnAssets", ratio),
        # return on equity
        "roe": fetch_metric("returnOnEquity", ratio),
        "net_income_per_ebt": fetch_metric("netIncomePerEBT", ratio),
        "debt_ratio": fetch_metric("debtRatio", ratio),
        "per": fetch_metric("priceEarningsRatio", ratio),
        "pbr": fetch_metric("priceToBookRatio", ratio),
        "psr": fetch_metric("priceToSalesRatio", ratio),
        "pcfr": fetch_metric("priceCashFlowRatio", ratio),
        "pegr": fetch_metric("priceEarningsToGrowthRatio", ratio),
        "revenue_growth": fetch_metric("revenueGrowth", growth),
        "gross_profit_growth": fetch_metric("grossProfitGrowth", growth),
        "ebit_growth": fetch_metric("ebitgrowth", growth),
        "operating_income_growth": fetch_metric("operatingIncomeGrowth", growth),
        "net_income_growth": fetch_metric("netIncomeGrowth", growth),
        "eps_growth": fetch_metric("epsgrowth", growth),
        "eps_diluted_growth": fetch_metric("epsdilutedGrowth", growth),
        "operating_cash_flow_growth": fetch_metric("operatingCashFlowGrowth", growth)
    }


def fetch_metric(key, data):
    return data[key] if key in data else 0
