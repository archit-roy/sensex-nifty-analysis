# ─────────────────────────────────────────────
#  Sensex & Nifty Analysis — CSV Export for Power BI
#  Author : Archit Roy
# ─────────────────────────────────────────────

import os
from fetch_data import fetch_index_data
from analysis   import run_all_analysis

os.makedirs("powerbi_data", exist_ok=True)

print("Fetching and analysing data...")
df = fetch_index_data()
returns, monthly, annual, volatility, risk, correlation = run_all_analysis(df)

# Daily data
daily = returns.reset_index()
daily.columns = [str(c) for c in daily.columns]
daily.to_csv("powerbi_data/daily.csv", index=False)
print("✅  daily.csv saved")

# Monthly data
mon = monthly.reset_index()
mon.columns = [str(c) for c in mon.columns]
mon.to_csv("powerbi_data/monthly.csv", index=False)
print("✅  monthly.csv saved")

# Annual data
ann = annual.reset_index()
ann.columns = [str(c) for c in ann.columns]
ann.to_csv("powerbi_data/annual.csv", index=False)
print("✅  annual.csv saved")

# Volatility data
vol = volatility.reset_index()
vol.columns = [str(c) for c in vol.columns]
vol.to_csv("powerbi_data/volatility.csv", index=False)
print("✅  volatility.csv saved")

# Risk metrics
risk.to_csv("powerbi_data/risk_metrics.csv")
print("✅  risk_metrics.csv saved")

print("\n✅  All CSVs saved to powerbi_data/ folder — ready for Power BI!")