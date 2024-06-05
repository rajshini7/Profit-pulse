# backend/models/lstm_gru_news_model.py
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, GRU, Dense, Dropout


def create_lstm_gru_news_model(input_shape):
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=input_shape))
    model.add(GRU(32))
    model.add(Dropout(0.2))
    model.add(Dense(1))

    model.compile(optimizer="adam", loss="mean_squared_error")
    return model


def train_model(X_train, y_train, input_shape, epochs=50, batch_size=32):
    model = create_lstm_gru_news_model(input_shape)
    model.fit(
        X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1
    )
    return model
