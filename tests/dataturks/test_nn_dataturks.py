import pandas as pd

from src.data.preprocess.dataturks.generate_nn_dataturks import split
from src.models.dataturks import predict_nn_dataturks as model

PATH_TO_DATA = "data/external/dataturks/example.csv"
PATH_TO_MODEL = "models/example_dataturks.h5"


def test_create_dictionary_vocab_size_is_correct(create_dataset_vocabulary):
    assert create_dataset_vocabulary.num_words == 10000


def test_create_dictionary_doesnt_remove_stopwords(create_dataset_vocabulary):
    assert "the" in create_dataset_vocabulary.word_counts.keys()
    assert "is" in create_dataset_vocabulary.word_counts.keys()
    assert "are" in create_dataset_vocabulary.word_counts.keys()


def test_create_dictionary_removes_punctuation(create_dataset_vocabulary):
    assert "!" not in create_dataset_vocabulary.word_counts.keys()
    assert ":)" not in create_dataset_vocabulary.word_counts.keys()
    assert "@" not in create_dataset_vocabulary.word_counts.keys()


def test_create_dictionary_removes_urls(create_dataset_vocabulary):
    assert "http" in create_dataset_vocabulary.word_counts.keys()


def test_create_dictionary_removes_unicode(create_dataset_vocabulary):
    assert "\\xa0" not in create_dataset_vocabulary.word_counts.keys()


def proportion(dataframe, label):
    return dataframe.loc[dataframe["label"] == label, "label"].count() / len(dataframe)


def test_split_data_is_representative_of_underlying_distribution():
    data = pd.read_csv(PATH_TO_DATA)

    n_1s = proportion(data, 1)
    n_0s = proportion(data, 0)

    train, test = split(data)

    n_train_1s = proportion(train, 1)
    n_train_0s = proportion(train, 0)

    n_test_1s = proportion(test, 1)
    n_test_0s = proportion(test, 0)

    assert round(n_train_1s, 1) == round(n_1s, 1)
    assert round(n_train_0s, 1) == round(n_0s, 1)

    assert round(n_test_1s, 1) == round(n_1s, 1)
    assert round(n_test_0s, 1) == round(n_0s, 1)


def test_basic_negative():
    assert (
        model.predict("You are a bitch", PATH_TO_MODEL, PATH_TO_DATA, "content", 10000)
        >= 0.5
    )
    assert (
        model.predict("Bitch suck dick", PATH_TO_MODEL, PATH_TO_DATA, "content", 10000)
        >= 0.5
    )
    assert (
        model.predict("I hate you", PATH_TO_MODEL, PATH_TO_DATA, "content", 10000)
        >= 0.5
    )


def test_basic_positive():
    assert (
        model.predict(
            "You are a lovely person", PATH_TO_MODEL, PATH_TO_DATA, "content", 10000
        )
        < 0.5
    )
    assert (
        model.predict(
            "The sun shines from your eyes",
            PATH_TO_MODEL,
            PATH_TO_DATA,
            "content",
            10000,
        )
        < 0.5
    )
    assert (
        model.predict(
            "I love you so much", PATH_TO_MODEL, PATH_TO_DATA, "content", 10000
        )
        < 0.5
    )
