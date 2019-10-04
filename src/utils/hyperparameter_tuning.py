"""
This file is an example, sadly not reusable yet
"""


from hyperopt import STATUS_OK
from hyperas.distributions import choice
from hyperopt import Trials, tpe
from hyperas import optim
from hyperas.distributions import choice, uniform
import pandas as pd
import keras
import numpy as np
import pandas as pd
import src.data.preprocess.dataturks.generate_nn_dataturks as preprocess
from keras.layers.core import Dense, Dropout, Activation
from keras.models import Sequential


def data():
    data = pd.read_csv("../../data/external/dataturks/example.csv")
    dictionary = preprocess.create_dictionary(data['text'], 10000)
    X_train_split, X_test_split = preprocess.split(data)
    y_train = X_train_split['label'].values
    y_test = X_test_split['label'].values

    x_train = keras.preprocessing.sequence.pad_sequences(dictionary.texts_to_sequences(X_train_split['text'].values), padding='post', maxlen=140)
    x_test = keras.preprocessing.sequence.pad_sequences(dictionary.texts_to_sequences(X_test_split['text'].values), padding='post', maxlen=140)
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

    model = Sequential()
    model.add(Dense(512, input_shape=(140,)))
    model.add(Activation('relu'))
    model.add(Dropout({{uniform(0, 1)}}))
    model.add(Dense({{choice([256, 512, 1024])}}))
    model.add(Activation({{choice(['relu', 'sigmoid'])}}))
    model.add(Dropout({{uniform(0, 1)}}))

    model.add(Dense(1))
    model.add(Activation('softmax'))

    model.compile(loss='binary_crossentropy', metrics=['accuracy'],
                  optimizer={{choice(['rmsprop', 'adam', 'sgd'])}})

    result = model.fit(x_train, y_train,
                       batch_size={{choice([64, 128])}},
                       epochs=2,
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
                                          trials=Trials(), verbose=True, keep_temp=True)
    X_train, Y_train, X_test, Y_test = data(path)
    print("Evalutation of best performing model:")
    print(best_model.evaluate(X_test, Y_test))
    print("Best performing model chosen hyper-parameters:")
    print(best_run)



