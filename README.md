# Momentum Strategy

The Momentum Strategy program is a Python-based tool that builds a momentum-driven portfolio using historical S&P 500 stock data.
Unlike value or equal-weighted models, this strategy selects companies that have shown the strongest recent price performance, based on the idea that stocks with upward momentum tend to continue performing well in the short term.

The script reads a list of S&P 500 stock tickers from a CSV file and retrieves each stock’s price history using the Yahoo Finance API.
It then calculates returns over different time horizons (1-year, 6-month, 3-month, and 1-month) to measure price momentum, ranks the results, and computes a High-Quality Momentum (HQM) Score that averages performance across all periods.

After ranking, the program asks the user to input the total value of their investment portfolio,
allocates equal capital to the top 50 momentum stocks,
and determines the number of shares to buy for each stock.

Finally, the program exports the results into a clean, formatted Excel spreadsheet
(momentum_strategy.xlsx) showing:

- Ticker symbol
- Stock price
- Multi-period returns and percentiles
- Calculated HQM Score
- Recommended number of shares to buy

This project is my practical introduction to quantitative investing and portfolio automation — combining data collection, statistical ranking, and trade allocation in one workflow.
