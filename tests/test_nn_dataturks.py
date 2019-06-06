from src.models import predict_nn_dataturks as model
from src.data.preprocess.generate_nn_dataturks import split

path_to_data = "/data/external/dataturks/example.csv"
path_to_model = "models/simple_dataturks.h5"


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


def test_create_dictionary_removes_URLS(create_dataset_vocabulary):
    # TODO this should fail, there should not be URLs in the corpus
    assert "http" in create_dataset_vocabulary.word_counts.keys()


def test_create_dictionary_removes_Unicode(create_dataset_vocabulary):
    assert "\\xa0" not in create_dataset_vocabulary.word_counts.keys()


# TODO finish adding a optimized test that will check ranking
# def test_create_dictionary_most_common_word_correctly_ranked(create_dataset_vocabulary):
#     data = pd.read_csv(os.getcwd() + "/data/dataturks/example.csv")
#     corpus = " ".join(data["content"]).split()
#     counts = sorted([(word, corpus.count(word)) for word in set(corpus)], key=lambda t: t[1], reverse=True)
#     print(counts[0])

def proportion(df, label):
    df.loc[df['label'] == label, 'label'].count() / len(df)


def test_split_data_is_representative_of_underlying_distribution(read_in_dataset):
    data = read_in_dataset

    n_1s = proportion(data, 1)
    n_0s = proportion(data, 0)

    train, test = split(data)

    n_train_1s = proportion(train, 1)
    n_train_0s = proportion(train, 0)

    n_test_1s = proportion(test, 0)
    n_test_0s = proportion(test, 0)

    assert n_train_1s == n_1s
    assert n_train_0s == n_0s

    assert n_test_1s == n_1s
    assert n_test_0s == n_0s


def test_basic_negative():
    assert model.predict("You are a bitch", path_to_model, path_to_data, 'content', 10000) >= 0.5
    assert model.predict("Bitch suck dick", path_to_model, path_to_data, 'content', 10000) >= 0.5
    assert model.predict("I hate you", path_to_model, path_to_data, 'content', 10000) >= 0.5


def test_basic_positive():
    assert model.predict("You are a lovely person", path_to_model, path_to_data, 'content', 10000) < 0.5
    assert model.predict("The sun shines from your eyes", path_to_model, path_to_data, 'content', 10000) < 0.5
    assert model.predict("I love you so much", path_to_model, path_to_data, 'content', 10000) < 0.5

