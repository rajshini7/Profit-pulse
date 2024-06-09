from textblob import TextBlob
import pandas as pd


def analyze_sentiment(text):
    analysis = TextBlob(text)
    return (
        "positive"
        if analysis.sentiment.polarity > 0
        else "negative" if analysis.sentiment.polarity < 0 else "neutral"
    )


def analyze_news_sentiment(news_data):
    print(news_data.columns)  # Inspect the columns

    # Ensure 'publishedAt' is the correct column name or adjust if necessary
    news_data["date"] = pd.to_datetime(news_data["publishedAt"])

    # Fill None values in 'description' with an empty string
    news_data["description"] = news_data["description"].fillna("")

    news_data["sentiment"] = news_data["description"].apply(analyze_sentiment)
    sentiment_data = news_data[["date", "sentiment"]]
    return sentiment_data
