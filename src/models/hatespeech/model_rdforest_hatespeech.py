import pandas as pd

from sklearn.model_selection import train_test_split
from src.data.preprocess.hatespeech.preprocess_rdforest_hatespeech import create_tfidf
from src.features.hatespeech.featureseng_rdforest_hatespeech import get_length_of_tweet
from src.utils.normalize import normalize

data = pd.read_csv("../../../data/external/hatespeech/hs_data.csv")

data['normalized'] = data['text'].apply(normalize)

X = create_tfidf(data['normalized'].to_list())['vectors']
y = pd.get_dummies(data['annotation'])['misogynistic']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% test

from sklearn.ensemble import RandomForestClassifier
#Create a Gaussian Classifier
clf=RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=None, max_features='auto', max_leaf_nodes=None,
            min_impurity_decrease=0.0, min_impurity_split=None,
            min_samples_leaf=1, min_samples_split=2,
            min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=1,
            oob_score=False, random_state=None, verbose=0,
            warm_start=False)

clf.fit(X_train,y_train)

# Feature importance
feature_names = create_tfidf(data['normalized'].to_list())['feature_names']
feature_imp = pd.Series(clf.feature_importances_, index=feature_names).sort_values(ascending=False)

y_pred=clf.predict(X_test)
from sklearn import metrics
# Model Accuracy, how often is the classifier correct?
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

import matplotlib.pyplot as plt
import seaborn as sns
# Creating a bar plot
sns.barplot(x=feature_imp[0:10], y=feature_imp.index[0:10])
# Add labels to your graph
plt.xlabel('Feature Importance Score')
plt.ylabel('Features')
plt.title("Visualizing Important Features")
plt.legend()
plt.show()


