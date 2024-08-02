from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from backend.data_collection.stock_data import fetch_stock_data, get_stock_data
from backend.data_collection.news_data import fetch_news_data
from backend.utils.data_preprocessing import preprocess_data
from backend.utils.sentiment_analysis import (
    analyze_news_sentiment,
    display_news_sentiment,
)
from backend.utils.plot_utils import (
    plot_line_chart,
    plot_candlestick_chart,
    plot_bar_chart,
)
from backend.models.frontendmodel import train_and_predict, print_dataset_info
import io
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

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
            or "date"  not in sentiment_data.columns
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


def fetch_stock_data(stock_ticker, start_date, end_date):
    try:
        # Fetch stock data using yfinance
        stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        print(f"Failed to fetch stock data: {e}")
        return pd.DataFrame()


def preprocess_data(stock_data):
    # Perform any necessary preprocessing here
    # For example, selecting relevant columns and ensuring datetime format
    if not stock_data.empty:
        stock_data.reset_index(inplace=True)
        stock_data["Date"] = pd.to_datetime(stock_data["Date"]).dt.strftime("%Y-%m-%d")
    return stock_data


def plot_line_chart(stock_data, img):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(stock_data["Date"], stock_data["Close"], label="Close Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title("Stock Price Over Time")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    canvas = FigureCanvas(fig)
    canvas.print_png(img)


def plot_candlestick_chart(stock_data, img):
    fig, ax = plt.subplots(figsize=(10, 6))
    stock_data["Date"] = stock_data["Date"].map(mdates.date2num)
    candlestick_ohlc(ax, stock_data.values, width=0.5, colorup="g", colordown="r")
    ax.xaxis_date()
    ax.set_title("Candlestick Chart")
    plt.xticks(rotation=45)
    plt.tight_layout()
    canvas = FigureCanvas(fig)
    canvas.print_png(img)


def plot_bar_chart(stock_data, img):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(stock_data["Date"], stock_data["Close"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Close Price")
    ax.set_title("Bar Chart")
    plt.xticks(rotation=45)
    plt.tight_layout()
    canvas = FigureCanvas(fig)
    canvas.print_png(img)


@app.route("/get_chart_data", methods=["GET"])
def get_chart_data():
    try:
        stock_ticker = request.args.get("stock_ticker", "").upper()
        if not stock_ticker:
            return jsonify({"error": "Stock ticker is required"}), 400

        chart_type = request.args.get("chart_type", "line")
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")

        # Fetch stock data
        stock_data = fetch_stock_data(stock_ticker, start_date, end_date)
        if stock_data.empty:
            return jsonify({"error": "Failed to fetch stock data."}), 500

        # Preprocess data
        processed_stock_data = preprocess_data(stock_data)

        img = io.BytesIO()
        if chart_type == "line":
            plot_line_chart(processed_stock_data, img)
        elif chart_type == "candlestick":
            plot_candlestick_chart(processed_stock_data, img)
        elif chart_type == "bar":
            plot_bar_chart(processed_stock_data, img)
        else:
            return jsonify({"error": f"Unsupported chart type: {chart_type}"}), 400

        img.seek(0)
        return send_file(img, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


import openai
from flask import Flask, jsonify, request
from flask_cors import CORS

CORS(app)


def get_chatbot_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages, max_tokens=150, temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        raise Exception(f"Error fetching chatbot response: {str(e)}")


@app.route("/chat", methods=["POST"])
def chatbot():
    try:
        data = request.get_json()
        message = data.get("message")
        if not message:
            return jsonify({"error": "Message is required"}), 400

        user_message = {"role": "user", "content": message}
        messages = [user_message]

        assistant_message = get_chatbot_response(messages)
        messages.append({"role": "assistant", "content": assistant_message})

        return jsonify({"response": assistant_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
