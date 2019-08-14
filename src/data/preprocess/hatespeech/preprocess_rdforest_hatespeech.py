from sklearn.feature_extraction.text import TfidfVectorizer

def generate_tfidf_vectors(corpus):
    """Returns the tf-idf vector representations of documents.
    Args:
        corpus (list) : A list of strings

    Returns:
        "vectors" (dict)  : The vectors
        "feature_names" (dict)  : The names of the features

    """
    vectorizer = TfidfVectorizer()
    return {"vectors": vectorizer.fit_transform(corpus), "feature_names": vectorizer.get_feature_names()}

