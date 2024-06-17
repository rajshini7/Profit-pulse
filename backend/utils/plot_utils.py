import matplotlib.pyplot as plt


def plot_loss(history):
    plt.figure(figsize=(10, 5))
    plt.plot(history.history["loss"], label="Training Loss")
    plt.title("Loss Curve")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()


def plot_accuracy_vs_epochs(epoch_values, mae_values):
    plt.figure(figsize=(10, 5))
    plt.plot(epoch_values, mae_values, label="MAE")
    plt.title("MAE vs Epochs")
    plt.xlabel("Epochs")
    plt.ylabel("MAE")
    plt.legend()
    plt.show()
