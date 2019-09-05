import pandas as pd


def evaluate(scores, targets):
    """Prints the f1-score and the confusion matrix for the model."""

    from sklearn.metrics import f1_score, confusion_matrix

    dataframe = pd.DataFrame({"score": pd.Series(scores)})
    dataframe.loc[dataframe['score'] >= 0.5, 'label'] = 1
    dataframe.loc[dataframe['score'] < 0.5, 'label'] = 0

    print(f1_score(targets, dataframe['label'].values))
    print(confusion_matrix(targets, dataframe['label'].values))
