import tensorflow as tf
import keras
from keras.callbacks import ModelCheckpoint, EarlyStopping


def create_model(word_embedding_matrix, vocab_size):
    in_dim, out_dim = word_embedding_matrix.shape

    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab_size, 40))
    model.add(
        keras.layers.Embedding(
            in_dim,
            out_dim,
            weights=[word_embedding_matrix],
            input_length=140,
            trainable=False,
        )
    )
    model.add(keras.layers.Dropout(0.1))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dropout(0.1))
    model.add(keras.layers.Dense(4, activation=tf.nn.relu))
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))
    # model.summary()

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["acc"])
    return model


def freeze_layers(model, n_layer):
    for layer in model.layers[0:n_layer]:
        layer.trainable = False
    return model


def get_callbacks(filename):
    callbacks = [
        ModelCheckpoint(filename, monitor="val_loss", save_best_only=True, mode="min"),
        EarlyStopping(monitor="val_loss", patience=5),
    ]
    return callbacks


def train_model(path_to_model, datasets, vocab_size):
    x_train, y_train = datasets[0], datasets[1]
    x_dev, y_dev = datasets[2], datasets[3]
    word_embedding_matrix = datasets[6]

    model = create_model(word_embedding_matrix, vocab_size)
    model.fit(
        x_train,
        y_train,
        epochs=50,
        batch_size=32,
        validation_data=(x_dev, y_dev),
        verbose=1,
        callbacks=get_callbacks(path_to_model),
    )
    print("Saved model to disk")


def fine_tune_model(path_to_model, path_to_fine_tuned_model, datasets, vocab_size):
    x_train, y_train = datasets[0], datasets[1]
    x_dev, y_dev = datasets[2], datasets[3]
    word_embedding_matrix = datasets[6]

    model = create_model(word_embedding_matrix, vocab_size)
    model.load_weights(path_to_model)
    model = freeze_layers(model, n_layer=-1)

    model.fit(
        x_train,
        y_train,
        epochs=50,
        batch_size=32,
        validation_data=(x_dev, y_dev),
        verbose=1,
        callbacks=get_callbacks(path_to_fine_tuned_model),
    )
    print("Saved model to disk")
