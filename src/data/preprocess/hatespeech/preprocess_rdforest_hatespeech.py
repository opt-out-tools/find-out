import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

path = "../../../../data/external/hatespeech/hs_data.csv"
data = pd.read_csv(path)



def create_tfidf(corpus):
    """Returns the tf-idf vector representations of documents.
    Args:
        corpus (list) : A list of strings

    Returns:
        vectors (scipy.sparse.csr.csr_matrix)  : The vectors

    """
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(corpus)
