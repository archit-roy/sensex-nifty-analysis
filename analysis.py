# ─────────────────────────────────────────────
#  Sensex & Nifty Analysis — Computations
#  Author : Archit Roy
# ─────────────────────────────────────────────

import pandas as pd
import numpy as np


def compute_returns(df):
    result = df.copy()
    result["Sensex_Daily_Return"] = df["Sensex"].squeeze().pct_change() * 100
    result["Nifty_Daily_Return"]  = df["Nifty"].squeeze().pct_change()  * 100
    result["Sensex_Cumulative"]   = ((df["Sensex"].squeeze() / df["Sensex"].squeeze().iloc[0]) - 1) * 100
    result["Nifty_Cumulative"]    = ((df["Nifty"].squeeze()  / df["Nifty"].squeeze().iloc[0])  - 1) * 100
    return result.round(4)


def compute_monthly(df):
    monthly = df[["Sensex", "Nifty"]].resample("ME").last()
    monthly.columns = ["Sensex", "Nifty"]
    monthly["Sensex_Monthly_Return"] = monthly["Sensex"].pct_change() * 100
    monthly["Nifty_Monthly_Return"]  = monthly["Nifty"].pct_change()  * 100
    return monthly.round(4)


def compute_annual(df):
    annual = df[["Sensex", "Nifty"]].resample("YE").last()
    annual.columns = ["Sensex", "Nifty"]
    annual["Sensex_Annual_Return"] = annual["Sensex"].pct_change() * 100
    annual["Nifty_Annual_Return"]  = annual["Nifty"].pct_change()  * 100
    annual.index = annual.index.year
    annual.index.name = "Year"
    # Flatten everything to plain floats
    for col in annual.columns:
        annual[col] = annual[col].apply(lambda x: round(float(x), 2) if pd.notna(x) else None)
    return annual


def compute_volatility(df):
    result = df.copy()
    daily_ret_s = df["Sensex"].squeeze().pct_change()
    daily_ret_n = df["Nifty"].squeeze().pct_change()
    result["Sensex_Vol_30D"] = daily_ret_s.rolling(30).std() * np.sqrt(252) * 100
    result["Sensex_Vol_90D"] = daily_ret_s.rolling(90).std() * np.sqrt(252) * 100
    result["Nifty_Vol_30D"]  = daily_ret_n.rolling(30).std() * np.sqrt(252) * 100
    result["Nifty_Vol_90D"]  = daily_ret_n.rolling(90).std() * np.sqrt(252) * 100
    return result.round(4)


def compute_risk_metrics(df):
    metrics = {}

    for index in ["Sensex", "Nifty"]:
        prices    = df[index].squeeze()
        daily_ret = prices.pct_change().dropna()

        total_return  = ((prices.iloc[-1] / prices.iloc[0]) - 1) * 100
        cagr          = ((prices.iloc[-1] / prices.iloc[0]) ** (1/10) - 1) * 100
        annual_vol    = daily_ret.std() * np.sqrt(252) * 100
        sharpe        = (daily_ret.mean() * 252) / (daily_ret.std() * np.sqrt(252))
        max_drawdown  = ((prices / prices.cummax()) - 1).min() * 100
        best_day      = daily_ret.max() * 100
        worst_day     = daily_ret.min() * 100
        positive_days = int((daily_ret > 0).sum())
        negative_days = int((daily_ret < 0).sum())
        win_rate      = (positive_days / len(daily_ret)) * 100

        metrics[index] = {
            "Start Price":           round(float(prices.iloc[0]), 2),
            "End Price":             round(float(prices.iloc[-1]), 2),
            "Total Return (%)":      round(float(total_return), 2),
            "CAGR (%)":              round(float(cagr), 2),
            "Annual Volatility (%)": round(float(annual_vol), 2),
            "Sharpe Ratio":          round(float(sharpe), 2),
            "Max Drawdown (%)":      round(float(max_drawdown), 2),
            "Best Day (%)":          round(float(best_day), 2),
            "Worst Day (%)":         round(float(worst_day), 2),
            "Positive Days":         positive_days,
            "Negative Days":         negative_days,
            "Win Rate (%)":          round(float(win_rate), 2),
        }

    return pd.DataFrame(metrics)


def compute_correlation(df):
    result = pd.DataFrame(index=df.index)
    s_ret  = df["Sensex"].squeeze().pct_change()
    n_ret  = df["Nifty"].squeeze().pct_change()
    result["Correlation_90D"] = s_ret.rolling(90).corr(n_ret)
    return result.round(4)


def run_all_analysis(df):
    print("Running analysis...")
    returns     = compute_returns(df)
    monthly     = compute_monthly(df)
    annual      = compute_annual(df)
    volatility  = compute_volatility(df)
    risk        = compute_risk_metrics(df)
    correlation = compute_correlation(df)
    print("✅  Analysis complete.")
    return returns, monthly, annual, volatility, risk, correlation


if __name__ == "__main__":
    from fetch_data import fetch_index_data
    df = fetch_index_data()
    returns, monthly, annual, volatility, risk, correlation = run_all_analysis(df)

    print("\n── Risk Metrics ─────────────────────────────")
    print(risk)

    print("\n── Annual Returns ───────────────────────────")
    print(annual[["Sensex_Annual_Return", "Nifty_Annual_Return"]])