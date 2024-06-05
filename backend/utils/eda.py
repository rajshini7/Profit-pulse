# backend/utils/eda.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from backend.config.config import PROCESSED_DATA_PATH


def load_data(file_path):
    return pd.read_csv(file_path, index_col="Date", parse_dates=True)


def summary_statistics(data):
    print("Summary Statistics:")
    print(data.describe())


def missing_values_analysis(data):
    print("Missing Values:")
    print(data.isnull().sum())


def plot_time_series(data):
    plt.figure(figsize=(14, 7))
    plt.plot(data["Close"])
    plt.title("Stock Closing Prices Over Time")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.show()


def plot_correlation_matrix(data):
    plt.figure(figsize=(10, 8))
    sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.show()


def plot_sentiment_analysis(data):
    sentiment_counts = data["Sentiment"].value_counts()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values)
    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Frequency")
    plt.show()


def main():
    file_path = os.path.join(PROCESSED_DATA_PATH, "merged_data.csv")
    data = load_data(file_path)

    summary_statistics(data)
    missing_values_analysis(data)
    plot_time_series(data)
    plot_correlation_matrix(data)
    plot_sentiment_analysis(data)


if __name__ == "__main__":
    main()
