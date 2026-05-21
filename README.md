# Sensex & Nifty Analysis (10 Years)

A multi-tool financial analysis project covering 10 years of BSE Sensex 
and NSE Nifty 50 index data. Built with Python for data processing, 
Excel for structured reporting, and Power BI for interactive dashboards.

---

## Project Structure
fetch_data.py        → fetches 10 years of daily data via Yahoo Finance
analysis.py          → computes returns, volatility, risk metrics
export.py            → writes formatted Excel report
export_csv.py        → exports CSVs for Power BI
sensex_nifty_analysis.xlsx   → Excel report (4 sheets)
sensex_nifty_dashboard.pbix  → Power BI dashboard (4 visuals)
---

## Analysis Covered

### Returns
- Daily returns for both indices
- Monthly closing prices and returns
- Year-wise annual returns (2016–2026)
- Cumulative returns from base period

### Risk Metrics
| Metric | Sensex | Nifty |
|---|---|---|
| CAGR (10Y) | 11.54% | 11.83% |
| Total Return | 197.99% | 205.97% |
| Annual Volatility | 16.38% | 16.26% |
| Sharpe Ratio | 0.77 | 0.79 |
| Max Drawdown | -38.07% | -38.44% |
| Win Rate | 53.68% | 54.17% |

### Volatility
- 30-day rolling volatility (annualised)
- 90-day rolling volatility (annualised)
- Rolling 90-day correlation between indices

---

## Excel Report — 4 Sheets
- **Risk Metrics** — side by side performance stats with color coding
- **Annual Returns** — year-wise returns table with bar chart
- **Monthly Data** — 120 months of closing prices and returns
- **Daily Data** — 500 days of daily prices, returns and cumulative returns

---

## Power BI Dashboard — 4 Visuals
- **Price History** — 10 year line chart of both indices
- **Annual Returns** — clustered bar chart by year
- **Volatility** — 30D rolling volatility line chart (COVID spike visible)
- **Risk Metrics Table** — all key stats side by side

---

## Setup

1. Install dependencies:
pip install yfinance pandas openpyxl matplotlib seaborn
2. Run full pipeline:
python fetch_data.py     # fetch data
python analysis.py       # run analysis
python export.py         # generate Excel
python export_csv.py     # generate CSVs for Power BI
3. Open `sensex_nifty_dashboard.pbix` in Power BI Desktop

---

## Key Findings

- Both indices delivered **~11.5% CAGR** over 10 years
- **COVID crash (2020)** caused a -38% max drawdown — clearly visible in volatility chart
- Markets recovered strongly in **2021 (+22% Sensex)**
- **2026 YTD is negative** (-11%) reflecting current market correction
- Sensex and Nifty are highly correlated — move almost identically

---

## Tech Stack

| Layer | Tool |
|---|---|
| Data Source | Yahoo Finance (yfinance) |
| Data Processing | Python, pandas, numpy |
| Reporting | Excel (openpyxl) |
| Dashboard | Power BI Desktop |
| Market | BSE Sensex + NSE Nifty 50 |

---

*Built by Archit Roy*