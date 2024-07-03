import yfinance as yf
import pandas as pd


def get_stock_data(ticker, period="1y", interval="1d"):
    """
    Fetch historical stock data for a given ticker symbol.

    Parameters:
    - ticker (str): The ticker symbol of the stock.
    - period (str): The period for which to fetch data. Default is '1y'.
    - interval (str): The interval of data points. Default is '1d'.

    Returns:
    - data (pd.DataFrame): DataFrame containing stock data.
    - error (str): Error message if fetching fails.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)

        if hist.empty:
            return None, f"No data found for ticker {ticker}."

        # Add additional features like Moving Averages if needed
        hist["MA20"] = hist["Close"].rolling(window=20).mean()
        hist["MA50"] = hist["Close"].rolling(window=50).mean()

        return hist, None
    except Exception as e:
        return None, str(e)


if __name__ == "__main__":
    ticker = input("Enter the stock ticker: ")
    data, error = get_stock_data(ticker)
    if data is not None:
        print(data.tail())
    else:
        print(f"Error: {error}")


def fetch_stock_data(stock_name, start_date, end_date):
    stock_data = yf.download(stock_name, start=start_date, end=end_date)
    print(stock_data.head())  # Add this line to inspect the columns
    return stock_data.reset_index()
