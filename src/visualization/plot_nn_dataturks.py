def plot(self, model):
    """Plots the accuracy and loss of the validation and training."""
    history_dict = model.history.history
    history_dict.keys()

    epochs = range(1, len(history_dict['acc']) + 1)

    plot_accuracy(epochs, history_dict['acc'], history_dict['val_acc'])
    plt.clf()
    plot_loss(epochs, history_dict['loss'], history_dict['val_loss'])



import matplotlib.pyplot as plt


def plot_loss(epochs, loss, val_loss):
    """Plots the loss of the training data."""
    # "bo" is for "blue dot"
    plt.plot(epochs, loss, 'bo', label='Training loss')
    # b is for "solid blue line"
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()


def plot_accuracy(epochs, acc, val_acc):
    """Plots the accuracy of the training data."""
    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.show()
