import matplotlib.pyplot as plt
import time
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
)


def plot_loss(history):
    plt.figure(figsize=(10, 6))
    plt.plot(history.history["loss"], label="Training Loss")
    plt.title("Loss Curve")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()


def plot_accuracy_vs_epochs(epoch_values, mae_values):
    plt.figure(figsize=(10, 6))
    plt.plot(epoch_values, mae_values, marker="o", label="MAE vs. Epochs")
    plt.title("MAE vs. Epochs")
    plt.xlabel("Epochs")
    plt.ylabel("Mean Absolute Error")
    plt.legend()
    plt.grid()
    plt.show()


def plot_training_time_vs_epochs(epoch_values, training_times):
    plt.figure(figsize=(10, 6))
    plt.plot(epoch_values, training_times, marker="o", label="Training Time vs. Epochs")
    plt.title("Training Time vs. Epochs")
    plt.xlabel("Epochs")
    plt.ylabel("Training Time (seconds)")
    plt.legend()
    plt.grid()
    plt.show()


def print_dataset_info(data, train_data_len):
    print("\nDataset Information:")
    print(f"Number of features: {data.shape[1]}")
    print(f"Feature names: {list(data.columns)}")
    print(f"Date range: {data.index.min()} to {data.index.max()}")
    print(f"Train/Test split: {train_data_len}/{len(data) - train_data_len}")
    print(data.describe())


def print_model_info(model):
    print("\nModel Architecture:")
    model.summary()
    total_params = model.count_params()
    print(f"Total parameters: {total_params}")
    print(f"Batch size: 1")
    print(f"Epochs: 100")


def detailed_error_analysis(y_test, predictions):
    errors = y_test - predictions
    percentage_errors = errors / y_test * 100
    plt.figure(figsize=(10, 6))
    plt.hist(percentage_errors, bins=50, edgecolor="k", alpha=0.7)
    plt.title("Distribution of Percentage Errors")
    plt.xlabel("Percentage Error")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    print("Error Analysis:")
    print(f"Mean Absolute Error: {mean_absolute_error(y_test, predictions):.4f}")
    print(f"Mean Squared Error: {mean_squared_error(y_test, predictions):.4f}")
    print(
        f"Root Mean Squared Error: {np.sqrt(mean_squared_error(y_test, predictions)):.4f}"
    )
    print(
        f"Mean Absolute Percentage Error: {mean_absolute_percentage_error(y_test, predictions):.4f}"
    )


def plot_error_analysis(y_test, predictions):
    errors = y_test - predictions
    plt.figure(figsize=(10, 6))
    plt.plot(y_test, label="True Values")
    plt.plot(predictions, label="Predicted Values")
    plt.title("True vs Predicted Values")
    plt.xlabel("Time")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.grid()
    plt.show()

    detailed_error_analysis(y_test, predictions)
