# backend/utils/data_preprocessing.py
import pandas as pd
import os
from backend.config.config import (
    RAW_STOCK_DATA_PATH,
    RAW_NEWS_DATA_PATH,
    PROCESSED_DATA_PATH,
)


def preprocess_stock_data(stock_file):
    stock_data = pd.read_csv(stock_file)
    stock_data["Date"] = pd.to_datetime(stock_data["Date"])
    stock_data.set_index("Date", inplace=True)
    return stock_data


def preprocess_news_data(news_file):
    news_data = pd.read_csv(news_file)
    news_data["Date"] = pd.to_datetime(news_data["Date"]).dt.date
    news_data["Sentiment"] = news_data["Sentiment"].apply(
        lambda x: 1 if x == "positive" else -1 if x == "negative" else 0
    )
    return news_data


def merge_data(stock_data, news_data):
    news_data["Date"] = pd.to_datetime(news_data["Date"])
    merged_data = pd.merge(stock_data, news_data, on="Date", how="left")
    merged_data.fillna(0, inplace=True)
    return merged_data


def preprocess_and_merge_data(stock_file, news_file, output_file):
    stock_data = preprocess_stock_data(stock_file)
    news_data = preprocess_news_data(news_file)
    merged_data = merge_data(stock_data, news_data)
    merged_data.to_csv(output_file)


if __name__ == "__main__":
    stock_file = os.path.join(RAW_STOCK_DATA_PATH, "stocks.csv")
    news_file = os.path.join(RAW_NEWS_DATA_PATH, "news.csv")
    output_file = os.path.join(PROCESSED_DATA_PATH, "merged_data.csv")

    preprocess_and_merge_data(stock_file, news_file, output_file)
    print("Data preprocessing and merging completed.")

# data_preprocessing.py

import pandas as pd


def preprocess_data(stock_data):
    # Example preprocessing steps, adjust as needed
    stock_data["date"] = pd.to_datetime(stock_data["date"])
    stock_data.set_index("date", inplace=True)
    stock_data["target"] = stock_data["Close"].shift(-1)
    stock_data.dropna(inplace=True)
    return stock_data
