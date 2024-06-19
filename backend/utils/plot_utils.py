import matplotlib.pyplot as plt

def plot_loss(history):
    plt.figure(figsize=(10, 6))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_accuracy_vs_epochs(epochs, accuracies):
    plt.figure(figsize=(10, 6))
    plt.plot(epochs, accuracies, marker='o', label='MAE')
    plt.title('Accuracy vs Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Mean Absolute Error (MAE)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_combined_loss(losses_dict):
    plt.figure(figsize=(10, 6))
    for epochs, losses in losses_dict.items():
        plt.plot(losses, label=f'{epochs} epochs')
    plt.title('Loss Curve for Different Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.show()

def detailed_layer_info(model):
    for i, layer in enumerate(model.layers):
        print(f"Layer {i+1}: {layer.name}")
        config = layer.get_config()
        for key, value in config.items():
            print(f"  {key}: {value}")
        layer_input_shape = (
            layer.input_shape
            if hasattr(layer, "input_shape")
            else layer.get_input_shape_at(0)
        )
        layer_output_shape = (
            layer.output_shape
            if hasattr(layer, "output_shape")
            else layer.get_output_shape_at(0)
        )
        print(f"  Input shape: {layer_input_shape}")
        print(f"  Output shape: {layer_output_shape}")


def print_dataset_info(data, train_data_len):
    print("\nDataset Information:")
    print(f"Number of features: {data.shape[1]}")
    print(f"Feature names: {list(data.columns)}")
    print(f"Date range: {data.index.min()} to {data.index.max()}")
    print(f"Train/Test split: {train_data_len}/{len(data) - train_data_len}")
    print(data.describe())