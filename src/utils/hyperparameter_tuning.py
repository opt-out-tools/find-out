from hyperopt import STATUS_OK
from hyperas.distributions import choice
import keras
import numpy as np
import pandas as pd
import src.data.preprocess.dataturks.generate_nn_dataturks as preprocess

def data():
    data = pd.read_csv("../../data/external/dataturks/example.csv")
    dictionary = preprocess.create_dictionary(data['content'], 10000)
    X_train, X_test = preprocess.split(data)
    Y_train = X_train['label']
    Y_test = X_test['label']

    X_padded_train = keras.preprocessing.sequence.pad_sequences(dictionary.texts_to_sequences(X_train['content'].values), padding='post', maxlen=140)
    X_padded_test = keras.preprocessing.sequence.pad_sequences(dictionary.texts_to_sequences(X_test['content'].values), padding='post', maxlen=140)
    return X_padded_train, X_padded_test, Y_train.values, Y_test.values

def create_model():
    """Returns the sentiment of the parsed sentence.

    Args:
        train_data (df) : The data the model is to be built from.
        save_word_embeddings (bool) : If true, will save the embedding data.
        save_model (bool) : If true, will save the model.

    Returns
        model : The sentiment analyser model, fit to the training data.
    """

    X_train, X_test, Y_train, Y_test = data()
    model = keras.Sequential()
    model.add(keras.layers.Embedding(10000, 40))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense({{choice([np.power(2, 5), np.power(2, 6), np.power(2, 7)])}}, input_shape=(140,)))
    model.add(keras.layers.Dense({{choice([np.power(2, 5), np.power(2, 6), np.power(2, 7)])}}, input_shape=(140,)))

    model.summary()

    split = int(len(X_train) / 4)  # number of comments halved

    x_val = X_train[:split]
    partial_X_train = X_train[split:]

    y_val = Y_train[:split]
    partial_y_train = Y_train[split:]

    from keras import callbacks

    reduce_lr = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2,
                                            patience=5, min_lr=0.001)

    model.compile(optimizer={{choice(['rmsprop', 'adam', 'sgd'])}},
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    model.fit(X_train,
              Y_train,
              epochs={{choice([25, 50, 75, 100])}},
              batch_size={{choice([16, 32, 64])}},
              callbacks=[reduce_lr])

    score, acc = model.evaluate(x_val, y_val, verbose=0)
    print('Test accuracy:', acc)
    return {'loss': -acc, 'status': STATUS_OK, 'model': model}
    return model




