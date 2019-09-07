"""
Train feedforward architecture.
"""

import os

import keras
import pandas as pd
import tensorflow as tf

from src.data.preprocess.dataturks.generate_nn_dataturks import split, create_dictionary


def build(path_to_data, text_column_name, label_column_name, hyperparameters):
    """Returns the built model. This function prepares the text, turns
    them into tensors, creates a word embedding and trains the neural
    net and build the final model. The model will always be saved.
    There is one flag that allow the embeddings to be saved.

    Args:
        path_to_data (str) : The path to the dataset.
        text_column_name (str) : The name of the column of the dataset
        with the text to be classified.
        label_column_name (str) : The name of the column of labels.
        hyperparameters (dict) : A dictionary of all of the
        hyperparameters for the model.

    Returns
        model : The sentiment analyser model, fit to the training data.
    """
    data = pd.read_csv(os.getcwd() + path_to_data)

    corpus_vocabulary = create_dictionary(
        data[text_column_name], hyperparameters["vocab_size"]
    )

    train, test = split(data)

    x_train = train[text_column_name]
    y_train = train[label_column_name]

    train_sequences = corpus_vocabulary.texts_to_sequences(x_train.values)
    padded_train = keras.preprocessing.sequence.pad_sequences(
        train_sequences, padding="post", maxlen=140
    )
    model = keras.Sequential()
    model.add(keras.layers.Embedding(hyperparameters["vocab_size"], 40))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(4, activation=tf.nn.relu))
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

    model.summary()

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["acc"])

    split_val = int(len(x_train) / 4)  # number of comments halved

    x_val = padded_train[:split_val]
    partial_x_train = padded_train[split_val:]

    y_val = y_train[:split_val]
    partial_y_train = y_train[split_val:]

    model.fit(
        partial_x_train,
        partial_y_train,
        epochs=hyperparameters["epoch"],
        batch_size=hyperparameters["batch_size"],
        validation_data=(x_val, y_val),
        verbose=hyperparameters["verbose"],
    )

    import datetime as dt

    now = dt.datetime.now().__str__()
    model.save(os.getcwd() + "../models/dataturks " + now + ".h5")
    print("Model saved.")
