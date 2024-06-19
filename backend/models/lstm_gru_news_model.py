import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, GRU
from backend.utils.plot_utils import (
    plot_loss,
    plot_accuracy_vs_epochs,
    plot_combined_loss,  # Import the new plotting function
)


def train_and_predict(combined_data, epochs=1):
    # Ensure 'Adj Close' column exists
    if "Adj Close" not in combined_data.columns:
        raise KeyError("'Adj Close' not found in combined_data columns")

    # Select features, including sentiment
    features = combined_data[
        ["Open", "High", "Low", "Close", "Adj Close", "Volume", "sentiment"]
    ].copy()
    target = combined_data["Adj Close"]

    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(features)

    # Prepare the training data
    train_data_len = int(np.ceil(len(scaled_data) * 0.8))
    train_data = scaled_data[0:train_data_len, :]
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i - 60 : i, :])
        y_train.append(
            train_data[i, 4]
        )  # 'Adj Close' is at index 4 in the selected features

    x_train, y_train = np.array(x_train), np.array(y_train)

    # Build the LSTM-GRU model
    model = Sequential()
    model.add(
        LSTM(
            units=50,
            return_sequences=True,
            input_shape=(x_train.shape[1], x_train.shape[2]),
        )
    )
    model.add(GRU(units=25, return_sequences=False))
    model.add(Dense(units=8))
    model.add(Dense(units=1))

    # Compile the model
    model.compile(optimizer="adam", loss="mean_squared_error")

    # Train the model
    history = model.fit(x_train, y_train, batch_size=1, epochs=epochs)

    # Prepare the testing data
    test_data = scaled_data[train_data_len - 60 :, :]
    x_test = []
    y_test = target[train_data_len:].values

    for i in range(60, len(test_data)):
        x_test.append(test_data[i - 60 : i, :])

    x_test = np.array(x_test)

    # Get the predicted prices
    predictions = model.predict(x_test)

    predictions_with_dummies = np.concatenate(
        [predictions, np.zeros((predictions.shape[0], scaled_data.shape[1] - 1))],
        axis=1,
    )
    predictions = scaler.inverse_transform(predictions_with_dummies)[:, 0]

    # Calculate metrics
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    mape = mean_absolute_percentage_error(y_test, predictions)
    rmse = np.sqrt(mse)

    # Print model summary
    return predictions[-1], mae, mse, rmse, mape, model, history.history["loss"]


def experiment_with_epochs(combined_data):
    epoch_values = [25, 50, 75, 100, 150]
    losses_dict = {}
    for epochs in epoch_values:
        _, mae, _, _, _, _, loss_history = train_and_predict(combined_data, epochs)
        losses_dict[epochs] = loss_history

    plot_combined_loss(losses_dict)


def print_model_info(model):
    print("\nModel Architecture:")
    model.summary()
    total_params = model.count_params()
    print(f"Total parameters: {total_params}")
    print(f"Batch size: 1")
    print(f"Epochs: 100")
