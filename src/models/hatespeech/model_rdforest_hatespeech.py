import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from src.data.preprocess.hatespeech.preprocess_rdforest_hatespeech import (
    generate_tfidf_vectors,
)
from src.features.hatespeech.featureseng_helperfunc_hatespeech import (
    combine_feature_space,
)
from src.features.hatespeech.featureseng_rdforest_hatespeech import (
    contains_not_sexist_but,
)
from src.utils.preprocess_text_helpers import normalizer

DATA = pd.read_csv("../../../DATA/external/hatespeech/hs_data.csv")

DATA["normalized"] = normalizer(DATA["text"])
X = generate_tfidf_vectors(DATA["normalized"].to_list())["vectors"]

DATA["contains_not_sexist_but"] = DATA["text"].apply(contains_not_sexist_but)
X = combine_feature_space(X, DATA["contains_not_sexist_but"].values)

Y = pd.get_dummies(DATA["annotation"])["misogynistic"]
X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = train_test_split(X, Y, test_size=0.3)

CLF = RandomForestClassifier(
    bootstrap=True,
    class_weight=None,
    criterion="gini",
    max_depth=None,
    max_features="auto",
    max_leaf_nodes=None,
    min_impurity_decrease=0.0,
    min_impurity_split=None,
    min_samples_leaf=1,
    min_samples_split=2,
    min_weight_fraction_leaf=0.0,
    n_estimators=100,
    n_jobs=1,
    oob_score=False,
    random_state=None,
    verbose=0,
    warm_start=False,
)

CLF.fit(X_TRAIN, Y_TRAIN)

FEATURE_NAMES = generate_tfidf_vectors(DATA["normalized"].to_list())[
    "FEATURE_NAMES"
] + ["contains_not_sexist_but"]
FEATURE_IMPORTANCE = pd.Series(
    CLF.feature_importances_, index=FEATURE_NAMES
).sort_values(ascending=False)

Y_PRED = CLF.predict(X_TEST)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:", metrics.accuracy_score(Y_TEST, Y_PRED))

# Creating a bar plot
sns.barplot(x=FEATURE_IMPORTANCE[0:10], y=FEATURE_IMPORTANCE.index[0:10])
# Add labels to your graph
plt.xlabel("Feature Importance Score")
plt.ylabel("Features")
plt.title("Visualizing Important Features")
plt.legend()
plt.show()
