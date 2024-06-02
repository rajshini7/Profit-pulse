import tweepy
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def fetch_tweets():
    try:
        # Authenticate to Twitter API
        auth = tweepy.OAuth1(
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_SECRET_KEY"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        )
        api = tweepy.API(auth, wait_on_rate_limit=True)

        # Fetch tweets related to stocks
        tweets = []
        for tweet in tweepy.Cursor(api.search_tweets, q="stock").items(
            100
        ):  # Adjust the number of tweets as needed
            tweets.append(tweet._json)
        tweets_df = pd.json_normalize(tweets)
        return tweets_df
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return None


if __name__ == "__main__":
    tweets_df = fetch_tweets()
    if tweets_df is not None:
        print(tweets_df.head())
    else:
        print("Failed to fetch tweets.")
