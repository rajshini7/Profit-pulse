# lstm_gru_news_model.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, GRU
from tensorflow.keras.layers import Dropout


def train_and_predict(data):
    data.set_index("date", inplace=True)
    features = data.drop(columns=["target"])
    target = data["target"]

    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(features)
    scaled_target = scaler.fit_transform(target.values.reshape(-1, 1))

    X_train, y_train = [], []

    for i in range(60, len(scaled_features) - 1):
        X_train.append(scaled_features[i - 60 : i])
        y_train.append(scaled_target[i])

    X_train, y_train = np.array(X_train), np.array(y_train)

    model = Sequential()
    model.add(
        LSTM(
            units=50,
            return_sequences=True,
            input_shape=(X_train.shape[1], X_train.shape[2]),
        )
    )
    model.add(Dropout(0.2))
    model.add(GRU(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(X_train, y_train, epochs=20, batch_size=32)

    last_60_days = scaled_features[-60:]
    X_test = np.array([last_60_days])
    predicted_price = model.predict(X_test)
    predicted_price = scaler.inverse_transform(predicted_price)

    return predicted_price[0][0]
