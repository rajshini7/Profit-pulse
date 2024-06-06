import os
import sys
from datetime import datetime, timedelta
import pandas as pd
from backend.config import config
from backend.data_collection.stock_data import fetch_stock_data
from backend.data_collection.news_data import fetch_news_data
from backend.utils.data_preprocessing import preprocess_data
from backend.utils.sentiment_analysis import analyze_news_sentiment
from backend.models.lstm_gru_news_model import train_and_predict


def main(stock_name):
    # Step 1: Fetch stock data
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    stock_data = fetch_stock_data(stock_name, start_date, end_date)
    if stock_data.empty:
        print(f"No stock data found for {stock_name}.")
        return

    # Step 2: Fetch news data
    news_data = fetch_news_data(stock_name)
    if news_data.empty:
        print(f"No news data found for {stock_name}.")
        return

    # Step 3: Preprocess data
    processed_stock_data = preprocess_data(stock_data)
    sentiment_data = analyze_news_sentiment(news_data)

    # Convert dates to match formats
    processed_stock_data["date"] = pd.to_datetime(processed_stock_data["date"])
    sentiment_data["date"] = pd.to_datetime(sentiment_data["date"]).dt.tz_localize(None)

    # Step 4: Add target column to stock data
    processed_stock_data["target"] = processed_stock_data["Close"].shift(-1)
    processed_stock_data = processed_stock_data.dropna()

    # Step 5: Combine datasets
    combined_data = pd.merge(
        processed_stock_data, sentiment_data, on="date", how="left"
    ).fillna(0)

    # Step 6: Train and predict
    predicted_price = train_and_predict(combined_data)

    print(f"Predicted price for {stock_name} for tomorrow is: {predicted_price}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <stock_name>")
        sys.exit(1)

    stock_name = sys.argv[1]
    main(stock_name)
