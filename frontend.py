from flask import Flask, request, jsonify, render_template
import yfinance as yf
import pandas as pd
import numpy as np
from backend.models.frontendmodel import train_and_predict, print_dataset_info
from datetime import datetime, timedelta

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

        # Fetch stock data
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
        stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
        if stock_data.empty:
            return jsonify({"error": "Failed to fetch stock data."})
        print(f"Stock data fetched for {stock_ticker}, data shape: {stock_data.shape}")

        # Add sentiment data
        stock_data["sentiment"] = 0.5  # Dummy sentiment data

        # Prepare combined data
        combined_data = stock_data.copy()
        combined_data.reset_index(inplace=True)
        combined_data.set_index("Date", inplace=True)

        # Print dataset info
        train_data_len = int(np.ceil(len(combined_data) * 0.8))
        print_dataset_info(combined_data, train_data_len)

        # Train and predict
        predicted_price, mae, mse, rmse, mape, model = train_and_predict(combined_data)
        sample_stock_data = stock_data.head(5).reset_index().to_dict(orient="records")

        response = {
            "today_price": stock_data["Adj Close"].iloc[-1],
            "tomorrow_prediction": predicted_price,
            "decision": (
                "BUY" if predicted_price > stock_data["Adj Close"].iloc[-1] else "DON'T BUY"
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
