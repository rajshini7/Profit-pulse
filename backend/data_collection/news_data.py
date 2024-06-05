from dotenv import load_dotenv
import os
from newsapi import NewsApiClient
import pandas as pd

# Load environment variables from .env file
load_dotenv()


def fetch_news(query, from_date, to_date, language="en", max_results=10):
    """
    Fetch news articles using the News API.

    Parameters:
    - query (str): Keywords to search for in news articles.
    - from_date (str): Start date in the format 'YYYY-MM-DD'.
    - to_date (str): End date in the format 'YYYY-MM-DD'.
    - language (str): Language of news articles (default is 'en' for English).
    - max_results (int): Maximum number of articles to fetch (default is 10).

    Returns:
    - news_df (pd.DataFrame): DataFrame containing fetched news articles.
    """
    # Fetch the API key from environment variables
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        raise ValueError(
            "News API key not found. Please set NEWS_API_KEY environment variable."
        )

    newsapi = NewsApiClient(api_key=api_key)

    # Fetch news articles
    news = newsapi.get_everything(
        q=query,
        from_param=from_date,
        to=to_date,
        language=language,
        page_size=max_results,
    )

    # Parse articles into DataFrame
    articles = []
    for article in news["articles"]:
        articles.append(
            {
                "source": article["source"]["name"],
                "author": article["author"],
                "title": article["title"],
                "description": article["description"],
                "url": article["url"],
                "published_at": article["publishedAt"],
            }
        )
    news_df = pd.DataFrame(articles)

    return news_df


if __name__ == "__main__":
    # Example usage
    query = input("Enter keywords to search for: ")
    from_date = input("Enter start date (YYYY-MM-DD, e.g., 2024-05-15): ")
    to_date = input("Enter end date (YYYY-MM-DD): ")

    news_df = fetch_news(query, from_date, to_date)
    print(news_df.head())

# news_data.py

import requests
import pandas as pd
from datetime import datetime, timedelta
from backend.config import config


def fetch_news_data(stock_name):
    url = f"https://newsapi.org/v2/everything?q={stock_name}&from={(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')}&sortBy=publishedAt&apiKey={config.NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    articles = data.get("articles", [])
    news_data = []

    for article in articles:
        news_data.append(
            {
                "date": article["publishedAt"][:10],
                "title": article["title"],
                "description": article["description"],
            }
        )

    return pd.DataFrame(news_data)
