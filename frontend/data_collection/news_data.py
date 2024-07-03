# backend/data_collection/news_data.py
import requests
import pandas as pd
from backend.config import config  # Ensure config is imported


def fetch_news_data(stock_name):
    url = (
        f"https://newsapi.org/v2/everything?q={stock_name}&apiKey={config.NEWS_API_KEY}"
    )
    response = requests.get(url)
    news_data = response.json()
    articles = news_data["articles"]
    news_df = pd.DataFrame(articles)
    print(news_df.head())  # Inspect the columns
    return news_df
