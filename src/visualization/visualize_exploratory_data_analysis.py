import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def plot_word_vectors(word_vectors, words, axis):
    """Plot a 2-D projection of the embeddings
    """
    pca = PCA(n_components=2)
    pca.fit(word_vectors)
    word_vecs_2d = pca.transform(word_vectors)

    axis.scatter(word_vecs_2d[:, 0], word_vecs_2d[:, 1])

    for word, coord in zip(words, word_vecs_2d):
        x, y = coord
        axis.text(x, y, word[0], size=15)

    axis.plot()
    plt.show()
    return axis
