# backend/utils/sentiment_analysis.py
from textblob import TextBlob


def analyze_sentiment(text):
    analysis = TextBlob(text)
    return (
        "positive"
        if analysis.sentiment.polarity > 0
        else "negative" if analysis.sentiment.polarity < 0 else "neutral"
    )
