import pandas as pd


def preprocess_data(data):
    print(data.columns)  # Inspect the columns
    data["date"] = pd.to_datetime(
        data["Date"]
    )  # Ensure 'Date' is the correct column name
    processed_data = data[
        ["date", "Open", "High", "Low", "Close", "Volume"]
    ]  # Adjust the column names if necessary
    processed_data = processed_data.dropna()  # Drop any rows with missing values
    return processed_data
