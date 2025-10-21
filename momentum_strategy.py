import numpy as np
import pandas as pd
import requests
import datetime as dt
import time
import math
from scipy import stats
import xlsxwriter
import yfinance as yf


# from my_secrets import API_KEY

stocks = pd.read_csv(r"C:\Users\vikra\OneDrive\Desktop\Python Trading Programs\Momentum Strategy\sp_500_stocks.csv")
print(stocks)

symbol = "AAPL"

try: 
    data = yf.download(symbol, period = "1y", progress = False, auto_adjust = False)
    # print(data.head())
    # print(data.tail())
    # print(data.info())
    # print(data.columns)               Was giving errors because the columns in yfinance dataframe doesn't have exact names 
    data.columns = [col[0] for col in data.columns]
    price_now = data["Close"].iloc[-1]
    price_year_ago = data["Close"].iloc[0]
    one_year_return = ((price_now - price_year_ago)/price_year_ago) * 100
    print(f"{symbol} 1-year Return: {one_year_return: .2f}%")
except Exception as e:
    one_year_return = "N/A"
    print(f"Error fetching data for {symbol}: {e}")


#Creating a dataframe for the data to go into
final_dataframe = pd.DataFrame(columns = ["Tickers", "Price", "1 year return (%)", "Number of Shares to Buy"])


#Looping through

end = dt.date.today()
start = end - dt.timedelta(days=365)

for symbol in stocks["Ticker"]:
    print(f"Fetching data for symbol: {symbol}")

    try:
        #downloading 1yr of data
        data = yf.download(symbol, start = start, end = end, progress = False, auto_adjust = True)

        if data.empty:
            print(f"No data for {symbol}")
            continue
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0] for col in data.columns]

        #calculating 1-yr returns
        price_year_ago = data["Close"].iloc[0]
        price_now = data["Close"].iloc[-1]
        one_year_return = ((price_now - price_year_ago)/price_year_ago) * 100

        #Appending to the dataframe
        new_row = pd.DataFrame({
            "Tickers" : [symbol], 
            "Price" : [price_now],
            "1 year return (%)" : [round(float(one_year_return), 2)]
        })
        final_dataframe = pd.concat([final_dataframe, new_row], ignore_index = True)

    except Exception as e:
        print(f"Error fetching symbol: {symbol}, error: {e}")
        continue
time.sleep(0.2)


final_dataframe.sort_values("1 year return (%)", ascending=False, inplace=True)
final_dataframe = final_dataframe[:50]
final_dataframe.reset_index(inplace=True)
print(final_dataframe)


def portfolio_input():
    global portfolio_size
    portfolio_size = input("Enter the size of your portfolio: ")

    try:
        float(portfolio_size)
    except ValueError:
        print("That is not a number! \nPlease try again: ")
        portfolio_size = input("Enter the size of your portfolio: ")

portfolio_input()

position_size = float(portfolio_size)/len(final_dataframe.index)
print(position_size)

for i in range(0, len(final_dataframe.index)):
    final_dataframe.loc[i, "Number of Shares to Buy"] = math.floor(position_size/final_dataframe.loc[i, "Price"])

print(final_dataframe)


#Making a high quality momentum strategy

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
    "One-Month Return Percentile"
]

hqm_dataframe = pd.DataFrame(columns = hqm_columns)
print(hqm_columns)