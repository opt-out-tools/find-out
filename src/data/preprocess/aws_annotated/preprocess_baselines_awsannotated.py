import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


def split_data(path):
    corpus = pd.read_csv(path)
    return train_test_split(corpus["text"], corpus["label"], test_size=0.33,
                            random_state=42)


if __name__ == "__main__":

    PATH = "../../../../data/external/aws_annotated/nlp_test_data.csv"
    COUNT_VECTORIZER = CountVectorizer()
    TFIDF_TRANSFORMER = TfidfTransformer()

    X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = split_data(PATH)

    TRAIN_TFIDF = TFIDF_TRANSFORMER.fit_transform(
        COUNT_VECTORIZER.fit_transform(X_TRAIN))

    MODEL = MultinomialNB().fit(TRAIN_TFIDF, Y_TRAIN)

    TEST_TFIDF = TFIDF_TRANSFORMER.transform(COUNT_VECTORIZER.transform(X_TEST))

    PREDICTED = MODEL.predict(TEST_TFIDF)

    for tweet, category in zip(X_TEST, PREDICTED):
        print("%r => %s" % (tweet, category))

    print(np.mean(PREDICTED == Y_TEST))
