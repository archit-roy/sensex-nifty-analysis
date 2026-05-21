# ─────────────────────────────────────────────
#  Sensex & Nifty Analysis — Excel Exporter
#  Author : Archit Roy
# ─────────────────────────────────────────────

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import LineChart, BarChart, Reference
from datetime import datetime


# ── Colors ─────────────────────────────────────
NAVY       = "1A1A2E"
GOLD       = "FFD700"
WHITE      = "FFFFFF"
LIGHT_GREY = "F2F2F2"
GREEN      = "C6EFCE"
RED        = "FFC7CE"
BLUE       = "BDD7EE"
DARK_BLUE  = "0F3460"


def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def font(color="000000", bold=False, size=10):
    return Font(color=color, bold=bold, size=size, name="Calibri")

def border():
    thin = Side(style="thin", color="D0D0D0")
    return Border(left=thin, right=thin, top=thin, bottom=thin)

def header_cell(cell, value, bg=NAVY, fg=GOLD, bold=True, size=10, align="center"):
    cell.value     = value
    cell.font      = Font(color=fg, bold=bold, size=size, name="Calibri")
    cell.fill      = fill(bg)
    cell.alignment = Alignment(horizontal=align, vertical="center")
    cell.border    = border()


# ── Sheet 1: Risk Metrics ──────────────────────
def write_risk_sheet(wb, risk_df):
    ws = wb.active
    ws.title = "Risk Metrics"
    ws.sheet_view.showGridLines = False

    # Title
    ws.merge_cells("A1:C1")
    header_cell(ws["A1"], "Sensex & Nifty — Risk & Performance Metrics (10 Years)", size=13)
    ws.row_dimensions[1].height = 28

    # Sub header
    for ci, val in enumerate(["Metric", "Sensex", "Nifty"], 1):
        header_cell(ws.cell(row=2, column=ci), val, bg=DARK_BLUE)
    ws.row_dimensions[2].height = 20

    # Column widths
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 16

    # Data
    for ri, (metric, row) in enumerate(risk_df.iterrows(), 3):
        bg = LIGHT_GREY if ri % 2 == 0 else WHITE
        ws.cell(row=ri, column=1, value=metric).fill  = fill(bg)
        ws.cell(row=ri, column=1).font    = font(bold=True, size=9)
        ws.cell(row=ri, column=1).border  = border()
        ws.cell(row=ri, column=1).alignment = Alignment(horizontal="left", vertical="center")

        for ci, val in enumerate([row["Sensex"], row["Nifty"]], 2):
            cell = ws.cell(row=ri, column=ci, value=val)
            cell.border    = border()
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font      = font(size=9)

            # Color positive/negative values
            if isinstance(val, float):
                if metric in ["Total Return (%)", "CAGR (%)", "Best Day (%)", "Win Rate (%)"]:
                    cell.fill = fill(GREEN)
                elif metric in ["Max Drawdown (%)", "Worst Day (%)"]:
                    cell.fill = fill(RED)
                else:
                    cell.fill = fill(bg)
            else:
                cell.fill = fill(bg)


# ── Sheet 2: Annual Returns ────────────────────
def write_annual_sheet(wb, annual_df):
    ws = wb.create_sheet("Annual Returns")
    ws.sheet_view.showGridLines = False

    ws.merge_cells("A1:E1")
    header_cell(ws["A1"], "Year-wise Annual Returns — Sensex & Nifty", size=13)
    ws.row_dimensions[1].height = 28

    headers = ["Year", "Sensex Close", "Nifty Close", "Sensex Return (%)", "Nifty Return (%)"]
    widths  = [10, 16, 16, 18, 18]
    for ci, (h, w) in enumerate(zip(headers, widths), 1):
        header_cell(ws.cell(row=2, column=ci), h, bg=DARK_BLUE)
        ws.column_dimensions[get_column_letter(ci)].width = w

    for ri, (year, row) in enumerate(annual_df.iterrows(), 3):
        bg = LIGHT_GREY if ri % 2 == 0 else WHITE
        values = [
            year,
            row["Sensex"],
            row["Nifty"],
            row["Sensex_Annual_Return"],
            row["Nifty_Annual_Return"],
        ]
        for ci, val in enumerate(values, 1):
            cell = ws.cell(row=ri, column=ci, value=val)
            cell.border    = border()
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font      = font(size=9)

            # Color return columns
            if ci in [4, 5] and isinstance(val, float):
                if val > 0:
                    cell.fill = fill(GREEN)
                else:
                    cell.fill = fill(RED)
            else:
                cell.fill = fill(bg)

    # Bar chart — annual returns
    chart = BarChart()
    chart.type    = "col"
    chart.title   = "Annual Returns (%)"
    chart.y_axis.title = "Return (%)"
    chart.style   = 10
    chart.width   = 22
    chart.height  = 14

    data = Reference(ws, min_col=4, max_col=5, min_row=2, max_row=len(annual_df)+2)
    cats = Reference(ws, min_col=1, min_row=3, max_row=len(annual_df)+2)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    ws.add_chart(chart, "G2")


# ── Sheet 3: Monthly Data ──────────────────────
def write_monthly_sheet(wb, monthly_df):
    ws = wb.create_sheet("Monthly Data")
    ws.sheet_view.showGridLines = False

    ws.merge_cells("A1:E1")
    header_cell(ws["A1"], "Monthly Closing Prices & Returns", size=13)
    ws.row_dimensions[1].height = 28

    headers = ["Date", "Sensex", "Nifty", "Sensex Return (%)", "Nifty Return (%)"]
    widths  = [14, 14, 14, 18, 18]
    for ci, (h, w) in enumerate(zip(headers, widths), 1):
        header_cell(ws.cell(row=2, column=ci), h, bg=DARK_BLUE)
        ws.column_dimensions[get_column_letter(ci)].width = w

    monthly_df = monthly_df.reset_index()
    for ri, row in enumerate(monthly_df.iterrows(), 3):
        _, r = row
        bg = LIGHT_GREY if ri % 2 == 0 else WHITE
        values = [
            str(r["Date"])[:10],
            r["Sensex"],
            r["Nifty"],
            r["Sensex_Monthly_Return"],
            r["Nifty_Monthly_Return"],
        ]
        for ci, val in enumerate(values, 1):
            cell = ws.cell(row=ri, column=ci, value=val)
            cell.border    = border()
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font      = font(size=9)
            cell.fill      = fill(bg)


# ── Sheet 4: Daily Data ────────────────────────
def write_daily_sheet(wb, returns_df):
    ws = wb.create_sheet("Daily Data")
    ws.sheet_view.showGridLines = False

    ws.merge_cells("A1:F1")
    header_cell(ws["A1"], "Daily Prices, Returns & Cumulative Returns", size=13)
    ws.row_dimensions[1].height = 28

    headers = ["Date", "Sensex", "Nifty", "Sensex Daily (%)", "Nifty Daily (%)", "Sensex Cumulative (%)"]
    widths  = [14, 12, 12, 18, 16, 22]
    for ci, (h, w) in enumerate(zip(headers, widths), 1):
        header_cell(ws.cell(row=2, column=ci), h, bg=DARK_BLUE)
        ws.column_dimensions[get_column_letter(ci)].width = w

    daily = returns_df.reset_index()
    for ri, (_, r) in enumerate(daily.iterrows(), 3):
        if ri > 502:   # limit to ~500 rows for performance
            break
        bg = LIGHT_GREY if ri % 2 == 0 else WHITE
        values = [
            str(r["Date"])[:10],
            r["Sensex"],
            r["Nifty"],
            r["Sensex_Daily_Return"],
            r["Nifty_Daily_Return"],
            r["Sensex_Cumulative"],
        ]
        for ci, val in enumerate(values, 1):
            cell = ws.cell(row=ri, column=ci, value=val)
            cell.border    = border()
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font      = font(size=9)
            cell.fill      = fill(bg)

    ws.freeze_panes = "A3"


# ── Main export function ───────────────────────
def export_to_excel(returns_df, monthly_df, annual_df, volatility_df, risk_df):
    print("Building Excel report...")

    wb = Workbook()
    write_risk_sheet(wb, risk_df)
    write_annual_sheet(wb, annual_df)
    write_monthly_sheet(wb, monthly_df)
    write_daily_sheet(wb, returns_df)

    filename = "sensex_nifty_analysis.xlsx"
    wb.save(filename)
    print("✅  Excel report saved: " + filename)


if __name__ == "__main__":
    from fetch_data import fetch_index_data
    from analysis   import run_all_analysis

    df = fetch_index_data()
    returns, monthly, annual, volatility, risk, correlation = run_all_analysis(df)
    export_to_excel(returns, monthly, annual, volatility, risk)