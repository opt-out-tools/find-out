from os.path import expanduser, exists
from zipfile import ZipFile

import keras
import numpy as np
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.utils.data_utils import get_file

KERAS_DATASETS_DIR = expanduser("~/.keras/datasets/")
GLOVE_ZIP_FILE_URL = "http://nlp.stanford.edu/data/glove.840B.300d.zip"
GLOVE_ZIP_FILE = "glove.840B.300d.zip"
GLOVE_FILE = "glove.840B.300d.txt"
EMBEDDING_DIM = 300


# Download and process GloVe embeddings
def download_glove():
    if not exists(KERAS_DATASETS_DIR + GLOVE_ZIP_FILE):
        zipfile = ZipFile(get_file(GLOVE_ZIP_FILE, GLOVE_ZIP_FILE_URL))
        zipfile.extract(GLOVE_FILE, path=KERAS_DATASETS_DIR)


def create_dictionary(data, n_words):
    """Prepares the corpus for the model and returns the Tokenizer object.
    Args:
        data (pandas series) : The column of text to be classified.
        n_words (int) : This argument will keep the most frequent n_words in the
        training data.

    Returns:
        tokenizer (Tokenizer) :
    """
    tokenizer = Tokenizer(num_words=n_words)
    tokenizer.fit_on_texts(data)
    return tokenizer


def split(data):
    """Randomly shuffles the data and splits it into train and test.
    Args:
        data (df) : The entire dataset.

    Returns:
        train (df) : The training data.
        test (df)  : The test data.
    """

    split_1 = int(0.6 * len(data))
    split_2 = int(0.8 * len(data))

    shuffled_data = data.sample(frac=1).reset_index(drop=True)
    train = shuffled_data[:split_1]
    dev = shuffled_data[split_1:split_2]
    test = shuffled_data[split_2:]
    return train, dev, test


# Create embedding index
def get_embeddings():
    embeddings_index = {}
    file = KERAS_DATASETS_DIR + GLOVE_FILE

    with open(file, encoding="utf-8") as f:
        for line in f:
            values = line.split(" ")
            word = values[0]
            embedding = np.asarray(values[1:], dtype="float32")
            embeddings_index[word] = embedding

    print("Word embeddings: %d" % len(embeddings_index))
    return embeddings_index


# Prepare word embedding matrix
def get_embedding_matrix(embeddings_index, word_index, max_nb_words):
    nb_words = min(max_nb_words, len(word_index))
    word_embedding_matrix = np.zeros((nb_words + 1, EMBEDDING_DIM))
    for word, i in word_index.items():
        if i > max_nb_words:
            continue
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            word_embedding_matrix[i] = embedding_vector

    print(
        "Null word embeddings: %d" % np.sum(np.sum(word_embedding_matrix, axis=1) == 0)
    )
    return word_embedding_matrix


# Initialize embedding matrix. If it exists, load it, otherwise create it
def init_embeddings(w_index, max_nb_words):
    cache_filename = "embedding_matrix.npy"

    if exists(cache_filename):
        word_embedding_matrix = np.load(cache_filename)
    else:
        # Prepare embedding matrix to be used in Embedding Layer
        embeddings_index = get_embeddings()
        word_embedding_matrix = get_embedding_matrix(
            embeddings_index, w_index, max_nb_words
        )
        np.save(cache_filename, word_embedding_matrix)
    return word_embedding_matrix


# Create word index
def get_word_index(tokenizer):
    word_index = tokenizer.word_index
    print("Words in index: %d" % len(word_index))

    return word_index


def create_NN_sets(path_to_data, vocab_size):
    data = pd.read_csv(path_to_data)
    corpus_vocabulary = create_dictionary(data["text"], vocab_size)

    train, dev, test = split(data)
    x_train, y_train = prepare_data(train, corpus_vocabulary)
    x_dev, y_dev = prepare_data(dev, corpus_vocabulary)
    x_test, y_test = prepare_data(test, corpus_vocabulary)

    word_index = corpus_vocabulary.word_index
    print("Words in index: %d" % len(word_index))
    word_embedding_matrix = init_embeddings(word_index, vocab_size)

    return [x_train, y_train, x_dev, y_dev, x_test, y_test, word_embedding_matrix]


def prepare_data(data, corpus_vocabulary):
    text = data["text"]
    label = data["label"]

    data_sequences = corpus_vocabulary.texts_to_sequences(text.values)
    padded_data = keras.preprocessing.sequence.pad_sequences(
        data_sequences, padding="post", maxlen=140
    )

    return padded_data, label
