#MomentumStrategy

This Python project builds and tests a momentum-based investment strategy using S&P 500 data. It includes two versions — a basic momentum strategy and a High-Quality Momentum (HQM) strategy that ranks stocks by performance across multiple time horizons.

#Files

- momentum_strategy.py – Calculates 1-year returns for all S&P 500 stocks, ranks them, and allocates equal capital to the top 50.
- hqm_strategy.py – Expands on the basic model by averaging percentile scores from 1-year, 6-month, 3-month, and 1-month returns to form an HQM Score.
- sp_500_stocks.csv – List of S&P 500 tickers used as input.
- momentum_strategy.xlsx – Example of the formatted output portfolio.

#Description

Both scripts pull historical stock data from Yahoo Finance using yfinance.
They calculate momentum returns, rank securities, and allocate an equal-weighted portfolio based on user-defined capital.
The results are exported into a styled Excel file using xlsxwriter.
