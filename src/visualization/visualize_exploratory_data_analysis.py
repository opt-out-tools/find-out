import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina', quality=100)


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


def rotate_ticks(graph1, graph2):
        for item1, item2 in zip(graph1.get_xticklabels(), graph2.get_xticklabels()):
            item1.set_rotation(90)
            item2.set_rotation(90)


def plot_two_barcharts(first_dataset, second_dataset, filepath, rotate_ticks=True):
    fig, ax = plt.subplots(ncols=2, figsize=(5, 5))

    first_plot = sns.barplot(x=first_dataset[0], y=first_dataset[1], ax=ax[0])
    second_plot = sns.barplot(x=second_dataset[0], y=second_dataset[1], ax=ax[1])

    if rotate_ticks == True:
        rotate_ticks(first_plot, second_plot)

    plt.savefig(filepath)
    plt.show()

    return fig, ax

def create_axis_object(fig, ax):
    # First, let's remove the top, right and left spines (figure borders)
    # which really aren't necessary for a bar chart.
    # Also, make the bottom spine gray instead of black.
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')

    # Second, remove the ticks as well.
    ax.tick_params(bottom=False, left=False)

    # Third, add a horizontal grid (but keep the vertical grid hidden).
    # Color the lines a light gray as well.
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)

    fig.tight_layout()

    return fig, ax
