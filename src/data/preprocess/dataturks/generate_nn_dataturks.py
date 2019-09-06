from keras.preprocessing.text import Tokenizer


def create_dictionary(data, n_words):
    """Prepares the corpus for the model and returns the Tokenizer
    object.
    Args:
        data (pandas series) : The column of text to be classified.
        n_words (int) : This argument will keep the most frequent
        n_words in the training data.

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
    where_to_split = int(len(data) * 0.8)
    shuffled_data = data.sample(frac=1).reset_index(drop=True)
    train = shuffled_data[:where_to_split]
    test = shuffled_data[where_to_split:]
    return train, test
