import time
import pandas as pd
import yfinance as yf

def fetch_stock_data(stocks, start_date, end_date, max_attempts=3, sleep_time=5):
    """
    Fetches adjusted close prices for each stock individually from Yahoo Finance.

    Parameters:
        stocks (list): List of stock ticker symbols.
        start_date (str): Start date in "YYYY-MM-DD" format.
        end_date (str): End date in "YYYY-MM-DD" format.
        max_attempts (int): Number of attempts to try for each stock.
        sleep_time (int): Number of seconds to wait between attempts.
        
    Returns:
        DataFrame: Stock data with dates as index.
    """
    data = {}
    for ticker in stocks:
        for attempt in range(1, max_attempts + 1):
            try:
                print(f"Fetching {ticker} (Attempt {attempt})...")
                ticker_data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)['Adj Close']
                
                if ticker_data.empty:
                    raise ValueError(f"No data for {ticker}")
                data[ticker] = ticker_data
                break
            except Exception as e:
                print(f"Error fetching {ticker}: {e}. Retrying in {sleep_time}s...")
                time.sleep(sleep_time)

        else:
            raise ValueError(f"Invalid Stock Ticker: {ticker}")

    return pd.concat(data, axis=1) if data else Exception("No stock data could be fetched.")