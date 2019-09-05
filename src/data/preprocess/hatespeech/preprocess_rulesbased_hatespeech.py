import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


def generate_count_vectors(corpus):
    """Returns the count vector representations of documents.
    Args:
        corpus (list) : A list of strings

    Returns:
        "vectors" (dict)  : The vectors
        "feature_names" (dict)  : The names of the features

    """
    vectorizer = CountVectorizer()
    return {
        "vectors": vectorizer.fit_transform(corpus),
        "feature_names": vectorizer.get_feature_names(),
    }


def count_corpus_word_frequency(corpus):
    """Plots a bar chart of the most common words in a corpus.
    Args:
        corpus (pandas series): corpus that has been normalized

    Returns:
        word_count: (pandas df) : words as index and their scores.
        Bar chart displaying 100 most common words.
    """
    words = corpus.str.split()
    word_counts = pd.value_counts(words.apply(pd.Series).stack())
    return pd.DataFrame(
        {"word": word_counts.index, "count": word_counts.values})
