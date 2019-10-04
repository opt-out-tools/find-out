import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns


def plot_word_vectors(word_vectors, words, ax):
    """
    """
    pca = PCA(n_components=2)
    pca.fit(word_vectors)
    word_vecs_2d = pca.transform(word_vectors)

    ax.scatter(word_vecs_2d[:, 0], word_vecs_2d[:, 1])

    for word, coord in zip(words, word_vecs_2d):
        X, Y = coord
        ax.text(X, Y, word[0], size=15)

    return ax

