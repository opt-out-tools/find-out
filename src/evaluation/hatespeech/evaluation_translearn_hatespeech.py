import matplotlib.pyplot as plt

from wordcloud import WordCloud
from src.models.hatespeech.model_translearn_hatespeech import create_model
from sklearn.metrics import f1_score, confusion_matrix

def get_predictions(model, test):
    y_pred = model.predict(test, batch_size=32)
    y_pred = (y_pred > 0.5)
    y_pred = y_pred.flatten()
    y_pred = y_pred.astype(int)
    return y_pred


def get_f1score(model, test, y_test):
    y_pred = get_predictions(model, test)

    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("Marco F1:%f" % f1_score(y_test, y_pred, average='macro'))
    print("Micro F1:%f" % f1_score(y_test, y_pred, average='micro'))
    print("Weighted F1:%f" % f1_score(y_test, y_pred, average='weighted'))


def evaluate_best_model(path_to_fine_tuned_model, x_test, y_test, word_embedding_matrix, vocab_size):
    best_model = create_model(word_embedding_matrix, vocab_size)
    best_model.load_weights(path_to_fine_tuned_model)
    scores = best_model.evaluate(x_test, y_test, verbose=1)
    print("%s: %.2f%%, %s: %.2f" % (best_model.metrics_names[1], scores[1] * 100, best_model.metrics_names[0], scores[0]))

    get_f1score(best_model, x_test, y_test)


def draw_wordcloud(data):
    """Draws a picture of a wordcloud with the data.
    Args:
        data (pandas df): the text to be used.
    Returns:
        Displays and saves wordcloud.
    """

    words = " ".join(sentence for sentence in data.to_list())

    return  WordCloud(background_color="white").generate(words)

def density_of_curse_words(tweet):
    """Returns the density of curse words.
    Args:
        tweet (str) :

    Returns:
        density (df) :
    """

    curse_words = ["fuck", "shit", "motherfucker", "crap", "ass", "bitch", "cunt"]

    tweet = tweet.split(" ")
    number_of_words = len(tweet)

    counts = {curse_word : tweet.count(curse_word) for curse_word in curse_words}
    for curse_word in counts:
        counts[curse_word] = counts[curse_word]/number_of_words
    return counts
