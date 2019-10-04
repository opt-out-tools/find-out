import json
import os

import numpy as np
import pandas as pd
import spacy

CURRENT_DIRECTORY = os.getcwd()
NLP = spacy.load("en_core_web_md")


def create_spacy_docs(data, label):
    """ Returns a dataframe of spacy docs."""

    return data[label].apply(lambda x: NLP(x))


def save_embeddings(model, word_index):
    """Writes two files to the current working directory containing the word
    embeddings and labels.

    Args:
        model (Sequential) : A sequential Keras model.
        word_index (dict) : The word to enumeration mapping.
    Returns:
         embeddings.tsv : The word embeddings for the model.
         metadata.tsv : The labels for the word embeddings.
    """

    embeddings = model.layers[0].get_weights()[0]
    np.savetxt(
        CURRENT_DIRECTORY + "/saved_model_data/embeddings/embedding.tsv",
        embeddings,
        delimiter="\t",
    )

    labels = np.array([key for key in word_index.keys()])
    np.savetxt(
        CURRENT_DIRECTORY + "/saved_model_data/embeddings/metadata.tsv",
        labels,
        delimiter="\t",
        fmt="%s",
    )


def is_correctly_labelled(scores, target_labels):
    """Returns the percentage of the test data that was correctly labelled.

    Args:
        scores (np.ndarray) : The predicted scores from the sentiment analyser.
        target_labels (np.ndarray) : The desired labelling from the
        sentiment analysers.

    Returns:
        float : The percentage of correctly labelled comments.
    """
    dataframe = pd.DataFrame(scores, columns={"score"})

    dataframe.loc[dataframe["score"] >= 0.5, "label"] = 1
    dataframe.loc[dataframe["score"] < 0.5, "label"] = 0

    hits_array = np.array(target_labels) == np.array(dataframe["label"].values)

    return round(float(np.sum(hits_array)) / len(target_labels) * 100, 2)


def convert_json_to_csv(read_filename, write_filename):
    """Converts a list of jsons which are not in correct list format,
    into the correct format and writes them to csv."""
    tweets = []
    for line in open(read_filename, "r"):
        tweets.append(json.loads(line))

    with open("tmp.json", "w") as outfile:
        json.dump(tweets, outfile)

    with open("tmp.json", encoding="utf-8") as data_file:
        data = json.loads(data_file.read())

    tmp = pd.DataFrame(data)
    tmp.to_csv(write_filename)
