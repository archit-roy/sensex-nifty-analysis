# ─────────────────────────────────────────────
#  Sensex & Nifty Analysis — Data Fetcher
#  Author : Archit Roy
# ─────────────────────────────────────────────

import yfinance as yf
import pandas as pd


def fetch_index_data():
    print("Fetching 10 years of Sensex and Nifty data...")

    sensex = yf.download("^BSESN", period="10y", interval="1d", auto_adjust=True)
    nifty  = yf.download("^NSEI",  period="10y", interval="1d", auto_adjust=True)

    # Flatten MultiIndex columns if present
    if isinstance(sensex.columns, pd.MultiIndex):
        sensex.columns = sensex.columns.get_level_values(0)
    if isinstance(nifty.columns, pd.MultiIndex):
        nifty.columns = nifty.columns.get_level_values(0)

    # Keep only closing prices
    sensex = sensex[["Close"]].rename(columns={"Close": "Sensex"})
    nifty  = nifty[["Close"]].rename(columns={"Close": "Nifty"})

    # Merge on date
    df = pd.merge(sensex, nifty, left_index=True, right_index=True, how="inner")
    df.index.name = "Date"

    # Flatten column MultiIndex if still present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Convert all columns to plain floats
    df["Sensex"] = df["Sensex"].astype(float).round(2)
    df["Nifty"]  = df["Nifty"].astype(float).round(2)

    print("✅  Fetched " + str(len(df)) + " trading days of data.")
    return df


if __name__ == "__main__":
    df = fetch_index_data()
    print(df.head())
    print(df.dtypes)