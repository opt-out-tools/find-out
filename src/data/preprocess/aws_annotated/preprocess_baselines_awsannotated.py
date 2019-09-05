import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

path = "../../../../data/external/aws_annotated/nlp_test_data.csv"
corpus = pd.read_csv(path)
targets = pd.get_dummies(corpus["annotation"])

x_train, x_test, y_train, y_test = train_test_split(
    corpus["text"], targets["misogynistic"], test_size=0.33, random_state=42
)

count_vect = CountVectorizer()
tfidf_transformer = TfidfTransformer()

x_train_counts = count_vect.fit_transform(x_train)
x_train_tfidf = tfidf_transformer.fit_transform(x_train_counts)
x_train_tfidf.shape

clf = MultinomialNB().fit(x_train_tfidf, y_train)

X_new_counts = count_vect.transform(x_test)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for tweet, category in zip(x_test, predicted):
    print("%r => %s" % (tweet, category))

print(np.mean(predicted == y_test))
