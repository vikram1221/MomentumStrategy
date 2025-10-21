import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta
import time
import math
from scipy import stats
from statistics import mean
import xlsxwriter
import yfinance as yf


stocks = pd.read_csv(r"C:\Users\vikra\OneDrive\Desktop\Python Trading Programs\Momentum Strategy\sp_500_stocks.csv")
#print(stocks)

#Making a high quality momentum strategy for these stocks

hqm_columns = [
    "Ticker", 
    "Price", 
    "Number of Shares to Buy", 
    "One-Year Price Return", 
    "One-Year Return Percentile", 
    "Six-Month Price Return", 
    "Six-Month Return Percentile",
    "Three-Month Price Return", 
    "Three-Month Return Percentile",
    "One-Month Price Return", 
    "One-Month Return Percentile", 
    "HQM Score"
]

hqm_dataframe = pd.DataFrame(columns = hqm_columns)
#print(hqm_columns)

end = datetime.today()
one_year_ago = end - timedelta(days=365)
six_months_ago = end - timedelta(days=182)
three_months_ago = end - timedelta(days=91)
one_month_ago = end - timedelta(days=30)

for symbol in stocks["Ticker"]:
    print(f"Fetching data for {symbol}")

    try:
        data = yf.download(symbol, start=one_year_ago, end=end, progress=False, auto_adjust=True)

        if data.empty:
            print(f"No data for {symbol}")
            continue

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0] for col in data.columns]

        price_now = data["Close"].iloc[-1]
        price_1yr = data["Close"].iloc[0] if len(data) > 250 else data["Close"].iloc[0]
        price_6mo = data.loc[data.index >= six_months_ago, "Close"].iloc[0]
        price_3mo = data.loc[data.index >= three_months_ago, "Close"].iloc[0]
        price_1mo = data.loc[data.index >= one_month_ago, "Close"].iloc[0]

        one_year_return = (price_now - price_1yr)/price_1yr
        six_month_return = (price_now - price_6mo)/price_6mo
        three_month_return = (price_now - price_3mo)/price_3mo
        one_month_return = (price_now - price_1mo)/price_1mo

        new_row = pd.Series([
            symbol, 
            round(price_now, 2),
            "N/A",
            round(one_year_return, 4),
            "N/A", 
            round(six_month_return, 4), 
            "N/A",
            round(three_month_return, 4),
            "N/A",
            round(one_month_return, 4),
            "N/A", 
            "N/A"
        ], index = hqm_columns)

        hqm_dataframe = pd.concat([hqm_dataframe, new_row.to_frame().T], ignore_index=True)

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        continue

time.sleep(0.2)

#print(hqm_dataframe)

time_periods = [
                "One-Year",
                "Six-Month", 
                "Three-Month", 
                "One-Month"
                ]

for row in hqm_dataframe.index:
    for time_period in time_periods:
        numeric_returns = pd.to_numeric(
            hqm_dataframe[f"{time_period} Price Return"], errors="coerce"
        )

        hqm_dataframe.loc[row, f"{time_period} Return Percentile"] = stats.percentileofscore(
            numeric_returns,
            hqm_dataframe.loc[row, f"{time_period} Price Return"]
        )/100

# print(hqm_dataframe)

#calculating the hqm score

for row in hqm_dataframe.index:
    momentum_percentiles = []
    for time_period in time_periods:
        momentum_percentiles.append(hqm_dataframe.loc[row, f"{time_period} Return Percentile"])
    hqm_dataframe.loc[row, "HQM Score"] = mean(momentum_percentiles)

#print(hqm_dataframe)

hqm_dataframe.sort_values("HQM Score", ascending=False, inplace=True)
hqm_dataframe = hqm_dataframe[:50]
hqm_dataframe.reset_index(inplace=True, drop=True)
#print(hqm_dataframe)


def portfolio_input():
    global portfolio_size
    portfolio_size = input("Enter the size of your portfolio: ")

    try:
        float(portfolio_size)
    except ValueError:
        print("That is not a number! \nPlease try again: ")
        portfolio_size = input("Enter the size of your portfolio: ")

portfolio_input()


position_size = float(portfolio_size)/len(hqm_dataframe.index)
print(position_size)

for i in hqm_dataframe.index:
    hqm_dataframe.loc[i, "Number of Shares to Buy"] = math.floor(position_size/hqm_dataframe.loc[i, "Price"])

print(hqm_dataframe)


#Exporting to an excel file

writer = pd.ExcelWriter("momentum_strategy.xlsx", engine="xlsxwriter")
hqm_dataframe.to_excel(writer, sheet_name="Momentum Strategy", index=False)

background_color = "#000000"
font_color = "#ffffff"

string_format = writer.book.add_format(
    {
        "font_color" : font_color,
        "bg_color" : background_color,
        "border" : 1 
    }
)

dollar_format = writer.book.add_format(
    {
        "num_format" : "$0.00",
        "font_color" : font_color,
        "bg_color" : background_color,
        "border" : 1 
    }
)

integer_format = writer.book.add_format(
    {
        "num_format" : "0",
        "font_color" : font_color,
        "bg_color" : background_color,
        "border" : 1 
    }
)

percent_fomat = writer.book.add_format(
    {
        "num_format": "0.0%",
        "font_color": font_color,
        "bg_color": background_color,
        "border": 1
    }
)

column_formats = {
    "A": ["Ticker", string_format], 
    "B": ["Price", dollar_format], 
    "C": ["Number of Shares to Buy", integer_format], 
    "D": ["One-Year Price Return", percent_fomat], 
    "E": ["One-Year Return Percentile", percent_fomat], 
    "F": ["Six-Month Price Return", percent_fomat], 
    "G": ["Six-Month Return Percentile", percent_fomat],
    "H": ["Three-Month Price Return", percent_fomat], 
    "I": ["Three-Month Return Percentile", percent_fomat],
    "J": ["One-Month Price Return", percent_fomat], 
    "K": ["One-Month Return Percentile", percent_fomat], 
    "L": ["HQM Score", percent_fomat]
}

for column in column_formats.keys():
    writer.sheets["Momentum Strategy"].set_column(f"{column}:{column}", 25, column_formats[column][1])
    writer.sheets["Momentum Strategy"].write(f"{column}1", column_formats[column][0], column_formats[column][1])

writer.close()