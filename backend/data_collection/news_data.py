import requests
import pandas as pd
from backend.config import config  # Ensure config is imported


def fetch_news_data(stock_name):
    """
    Fetch news data for a given stock name from the NewsAPI.

    Parameters:
    - stock_name (str): The name of the stock to fetch news for.

    Returns:
    - news_df (pd.DataFrame): DataFrame containing news articles.
    """
    url = (
        f"https://newsapi.org/v2/everything?q={stock_name}&apiKey={config.NEWS_API_KEY}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        news_data = response.json()
        articles = news_data.get("articles", [])
        news_df = pd.DataFrame(articles)
        return news_df
    except requests.RequestException as e:
        # Log the error (requires logging setup)
        print(f"Error fetching news data: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    stock_name = input("Enter the stock name: ")
    news_df = fetch_news_data(stock_name)
    print(news_df.head())
