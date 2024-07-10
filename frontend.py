from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from backend.data_collection.stock_data import fetch_stock_data, get_stock_data
from backend.data_collection.news_data import fetch_news_data
from backend.utils.data_preprocessing import preprocess_data
from backend.utils.sentiment_analysis import (
    analyze_news_sentiment,
    display_news_sentiment,
)
from backend.models.frontendmodel import train_and_predict, print_dataset_info

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
    template_folder="templates",
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        stock_ticker = data["stock_ticker"].upper()
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")

        # Fetch stock data
        stock_data = fetch_stock_data(stock_ticker, start_date, end_date)
        if stock_data.empty:
            print(f"No stock data found for {stock_ticker}.")
            return

        # Debugging: print fetched stock data
        print("Fetched stock data:", stock_data.head())

        # Fetch news data
        news_data = fetch_news_data(stock_ticker)
        if news_data.empty:
            return jsonify({"error": "No news data found."})

        # Debugging: print fetched news data
        print("Fetched news data:", news_data.head())

        # Process stock data
        processed_stock_data = preprocess_data(stock_data)

        # Debugging: print processed stock data
        print("Processed stock data:", processed_stock_data.head())

        # Analyze sentiment
        sentiment_data = analyze_news_sentiment(news_data)

        # Debugging: print sentiment data
        print("Sentiment data:", sentiment_data.head())

        processed_stock_data["date"] = pd.to_datetime(processed_stock_data["date"])
        sentiment_data["date"] = pd.to_datetime(sentiment_data["date"]).dt.tz_localize(
            None
        )

        # Ensure 'date' column is present
        if (
            "date" not in processed_stock_data.columns
            or "date" not in sentiment_data.columns
        ):
            return jsonify({"error": "Date column missing in processed data."})

        processed_stock_data["target"] = processed_stock_data["Close"].shift(-1)
        processed_stock_data = processed_stock_data.dropna()

        if "Adj Close" not in processed_stock_data.columns:
            processed_stock_data["Adj Close"] = processed_stock_data["Close"]

        combined_data = pd.merge(
            processed_stock_data, sentiment_data, on="date", how="left"
        ).fillna(0)
        combined_data.set_index("date", inplace=True)

        # Debugging: print combined data
        print("Combined data:", combined_data.head())

        train_data_len = int(np.ceil(len(combined_data) * 0.8))
        print_dataset_info(combined_data, train_data_len)

        predicted_price, mae, mse, rmse, mape, model = train_and_predict(combined_data)
        sample_stock_data = stock_data.head(5).reset_index().to_dict(orient="records")

        response = {
            "today_price": stock_data["Adj Close"].iloc[-1],
            "tomorrow_prediction": predicted_price,
            "decision": (
                "BUY"
                if predicted_price > stock_data["Adj Close"].iloc[-1]
                else "DON'T BUY"
            ),
            "certainty": 100 - mape,
            "stock_data_sample": sample_stock_data,
            "stock_data": stock_data.reset_index().to_dict(orient="records"),
            "news_data": news_data.head(5).to_dict(orient="records"),
        }
        return jsonify(response)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)})


@app.route("/recent_news", methods=["GET"])
def recent_news():
    stock_ticker = request.args.get("stock_ticker").upper()
    news_data = fetch_news_data(stock_ticker)
    if news_data.empty:
        return jsonify({"error": "No news data found."})
    news_data = display_news_sentiment(news_data)
    print(news_data.head())
    return jsonify(news_data.head(5).to_dict(orient="records"))


@app.route("/recent_stock_data", methods=["GET"])
def recent_stock_data():
    stock_ticker = request.args.get("stock_ticker").upper()
    stock_data, error = get_stock_data(stock_ticker)
    if stock_data is None:
        return jsonify({"error": error})
    return jsonify(stock_data.tail(5).reset_index().to_dict(orient="records"))


@app.route("/recent_stock_chart", methods=["GET"])
def recent_stock_chart():
    stock_ticker = request.args.get("stock_ticker").upper()
    stock_data, error = get_stock_data(stock_ticker)
    if stock_data is None:
        return jsonify({"error": error})
    stock_chart_data = {
        "labels": stock_data.index.strftime("%Y-%m-%d").tolist(),
        "prices": stock_data["Adj Close"].tolist(),
    }
    return jsonify(stock_chart_data)


if __name__ == "__main__":
    app.run(debug=True)
