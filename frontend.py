from flask import Flask, request, jsonify, render_template
import os
import sys
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from backend.config import config
from backend.data_collection.stock_data import fetch_stock_data
from backend.data_collection.news_data import fetch_news_data
from backend.utils.data_preprocessing import preprocess_data
from backend.utils.sentiment_analysis import analyze_news_sentiment
from backend.models.frontendmodel import (
    train_and_predict,
)

app = Flask(__name__, static_url_path="/static")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        stock_ticker = data["stock_ticker"].upper()
        print(f"Received request for stock ticker: {stock_ticker}")

        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
        stock_data = fetch_stock_data(stock_ticker, start_date, end_date)
        if stock_data.empty:
            return jsonify({"error": "Failed to fetch stock data."})
        print(f"Stock data fetched for {stock_ticker}, data shape: {stock_data.shape}")

        news_data = fetch_news_data(stock_ticker)
        if news_data.empty:
            print(f"No news data found for {stock_ticker}.")
            return

        # Step 3: Preprocess data
        processed_stock_data = preprocess_data(stock_data)
        sentiment_data = analyze_news_sentiment(news_data)

        # Convert dates to match formats
        processed_stock_data["date"] = pd.to_datetime(processed_stock_data["date"])
        sentiment_data["date"] = pd.to_datetime(sentiment_data["date"]).dt.tz_localize(
            None
        )

        # Step 4: Add target column to stock data
        processed_stock_data["target"] = processed_stock_data["Close"].shift(-1)
        processed_stock_data = processed_stock_data.dropna()

        # Check if 'Adj Close' column is present
        if "Adj Close" not in processed_stock_data.columns:
            processed_stock_data["Adj Close"] = processed_stock_data["Close"]

        # Step 5: Combine datasets
        combined_data = pd.merge(
            processed_stock_data, sentiment_data, on="date", how="left"
        ).fillna(0)
        combined_data.set_index("date", inplace=True)

        # Print dataset info
        train_data_len = int(np.ceil(len(combined_data) * 0.8))

        # Train and predict
        predicted_price, model = train_and_predict(combined_data)
        sample_stock_data = stock_data.head(5).reset_index().to_dict(orient="records")

        response = {
            "today_price": stock_data["Adj Close"].iloc[-1],
            "tomorrow_prediction": predicted_price,
            "decision": (
                "BUY" if predicted_price > stock_data["Adj Close"].iloc[-1] else "SELL"
            ),
            "stock_data_sample": sample_stock_data,
            "stock_data": stock_data.reset_index().to_dict(orient="records"),
        }
        return jsonify(response)

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
