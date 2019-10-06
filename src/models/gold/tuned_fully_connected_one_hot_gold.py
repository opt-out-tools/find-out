import numpy as np
import pandas as pd
from hyperas import optim
from hyperopt import STATUS_OK
from hyperopt import Trials
from hyperopt import tpe
from hyperopt.pyll.stochastic import choice
from keras import models
from keras.preprocessing.text import Tokenizer
import keras_metrics as km
from sklearn.model_selection import train_test_split
from keras import layers


def data():
    gold_data = pd.read_csv("../../../data/benchmark/gold/gold_data_en.csv")

    train_data, test_data, train_labels, test_labels = train_test_split(
        gold_data['text'], gold_data['label'], test_size=0.2)


    tokenizer = Tokenizer(num_words=10000)
    tokenizer.fit_on_texts(train_data)

    data = tokenizer.texts_to_matrix(train_data, mode='binary')

    # Prepare labels, transform to binary and float32
    # labels = train_labels.astype('float32')
    labels = train_labels.values

    # =========================
    # Split data
    # =========================

    # Randomly shuffle data
    indices = np.arange(data.shape[0])
    np.random.shuffle(indices)
    data = data[indices]
    labels = labels[indices]

    # Split into training and validation data (approximately 80:20)
    x_train = data
    y_train = labels

    x_test = tokenizer.texts_to_matrix(test_data, mode='binary')
    y_test = test_labels

    return x_train, y_train, x_test, y_test


def create_model(x_train, y_train):
    """
    Model providing function:

    Create Keras model with double curly brackets dropped-in as needed.
    Return value has to be a valid python dictionary with two customary keys:
        - loss: Specify a numeric evaluation metric to be minimized
        - status: Just use STATUS_OK and see hyperopt documentation if not feasible
    The last one is optional, though recommended, namely:
        - model: specify the model just created so that we can later use it again.
    """

    model = models.Sequential()
    model.add(layers.Dense({{choice([256, 512, 1024])}}, activation='relu', input_shape=(10000,)))
    model.add(layers.Dense({{choice([256, 512, 1024])}}))
    model.add(layers.Activation({{choice(['relu', 'sigmoid'])}}))
    model.add(layers.Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', metrics=['accuracy', km.binary_precision(), km.binary_recall()],
                  optimizer={{choice(['rmsprop', 'adam', 'sgd'])}})

    result = model.fit(x_train, y_train,
                       batch_size={{choice([64, 128])}},
                       epochs=200,
                       verbose=0,
                       validation_split=0.1)

    # get the highest validation accuracy of the training epochs
    validation_acc = np.amax(result.history['val_acc'])
    print('Best validation acc of epoch:', validation_acc)
    return {'loss': -validation_acc, 'status': STATUS_OK, 'model': model}

if __name__ == '__main__':
    best_run, best_model = optim.minimize(model=create_model,
                                          data=data,
                                          algo=tpe.suggest,
                                          max_evals=5,
                                          trials=Trials(), verbose=True)
    X_train, Y_train, X_test, Y_test = data()
    print("Evalutation of best performing model:")
    print(best_model.evaluate(X_test, Y_test))
    print("Best performing model chosen hyper-parameters:")
    print(best_run)

qcf
