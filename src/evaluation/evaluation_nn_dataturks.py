import pandas as pd

def evaluate(self, scores, targets):
    """Prints the f1-score and the confusion matrix for the model."""

    from sklearn.metrics import f1_score, confusion_matrix

    df = pd.DataFrame({"score": pd.Series(scores)})
    df.loc[df['score'] >= 0.5, 'label'] = 1
    df.loc[df['score'] < 0.5, 'label'] = 0

    print(f1_score(targets, df['label'].values))
    print(confusion_matrix(targets, df['label'].values))
