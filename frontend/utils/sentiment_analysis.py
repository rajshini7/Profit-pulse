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

    # Debugging: Print the first few descriptions to check the text data
    print("\nNews descriptions:")
    print(news_data["description"].head())

    # Apply sentiment analysis
    news_data["sentiment"] = news_data["description"].apply(analyze_sentiment)

    # Debugging: Print the sentiment values to check if they are being generated correctly
    print("\nSentiment analysis:")
    print(news_data[["description", "sentiment"]].head())

    # Map sentiment to numerical values
    sentiment_mapping = {"positive": 1, "negative": -1, "neutral": 0}
    news_data["sentiment"] = news_data["sentiment"].map(sentiment_mapping)

    # Debugging: Print the sentiment values after mapping to numerical values
    print("\nSentiment analysis (numerical):")
    print(news_data[["description", "sentiment"]].head())

    sentiment_data = news_data[["date", "sentiment"]]
    return sentiment_data

# Test the sentiment analysis with some sample data
if __name__ == "__main__":
    sample_news_data = pd.DataFrame({
        "publishedAt": ["2023-06-18T12:34:56Z", "2023-06-19T15:30:00Z"],
        "description": ["The stock market is very bad", "There are concerns about the economy."]
    })

    sentiment_data = analyze_news_sentiment(sample_news_data)
    print("\nSentiment Data:")
    print(sentiment_data)
