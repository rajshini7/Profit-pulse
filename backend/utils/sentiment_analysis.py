# backend/utils/sentiment_analysis.py
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
    sentiments = []

    for _, row in news_data.iterrows():
        sentiment = analyze_sentiment(row["title"] + " " + row["description"])
        sentiments.append({"date": row["date"], "sentiment": sentiment})

    return pd.DataFrame(sentiments)


if __name__ == "__main__":
    # For testing purpose
    test_data = pd.DataFrame(
        {
            "date": ["2024-06-05", "2024-06-05"],
            "title": ["Stock market rises", "Stock market falls"],
            "description": [
                "The stock market saw a significant rise today.",
                "The stock market saw a significant fall today.",
            ],
        }
    )

    result = analyze_news_sentiment(test_data)
    print(result)
