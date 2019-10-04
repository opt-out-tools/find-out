import re

import networkx as nx
import numpy as np
import pandas as pd
from spacy.symbols import VERB


def density_of_curse_words_in_sentence(tweet):
    """Returns the density of top 20 curse words, taken from Wang, Wenbo,  et  al.
    Cursing  in english on  twitter."
    The method needs the punctuation to be removed.
    Args:
        tweet (str) : the tweet to be counted.
    Returns:
        density (dict) : the curse words and their densities.
    """
    curse_words = [
        "fuck",
        "shit",
        "ass",
        "bitch",
        "nigga",
        "hell",
        "whore",
        "dick",
        "piss",
        "pussy",
        "slut",
        "puta",
        "tit",
        "damn",
        "fag",
        "cunt",
        "cum",
        "cock",
        "blowjob",
    ]

    # here we are going to use above words as roots in dictionary and then
    # as dictionary value add them and their plurals in order to make magic happen
    # I'm just adding plural but you can easily extend it with synonyms and such

    curse_roots = {
        curse_word: [curse_word, f"{curse_word}s"] for curse_word in curse_words
    }

    # now we create look_up dictionary which is a reverse of above (all values become
    # keys, and key become values)
    lookup = {}
    for key, values in curse_roots.items():
        for value in values:
            lookup[value] = key
    # here we add counter
    counts = {curse: 0 for curse in curse_words}

    #####
    tweet_words = tweet.lower().split(" ")
    # cleaning up white space
    tweet_words = [tweet_word.strip() for tweet_word in tweet_words]

    # now we just need to count how many times is each curse root used
    for word in tweet_words:
        if word in lookup:
            counts[lookup[word]] += 1

    # all done, now we just need frequency
    for key in counts:
        counts[key] /= len(tweet_words)
    return counts


def density_of_curse_words_in_total_corpus(dataframe, dataset_title):
    """Returns density of curse words across an entire corpus

      Args:
        dataframe (pandas df) : the df with the tweets to be counted.

    Returns:
        df (pandas df) : the curse words and their densities.

    """
    dataframe["curse_words"] = dataframe["text"].apply(
        density_of_curse_words_in_sentence
    )
    count = pd.DataFrame(list(dataframe["curse_words"])).T.sum(axis=1) / len(dataframe)
    return pd.DataFrame({dataset_title: count}, index=count.index)


def generate_ngrams(tweet, ngram_number):
    """Returns the n-grams in a sentence.

    Args:
        tweet (str) : the tweet to be grammed.
        ngram_number (int) : the number of grams, 2 = bigram, 3 = trigram.

    Returns
        bigrams (list) : a list of bigrams

    """
    tweet = tweet.lower()
    tweet = re.sub(r"[^a-zA-Z0-9\s]", " ", tweet)

    # Break sentence in the token, remove empty tokens
    tokens = [token for token in tweet.split(" ") if token != ""]

    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(ngram_number)])
    return [" ".join(ngram) for ngram in ngrams]


def tweet_legnth(data):
    data["tweet_length"] = data["text"].apply(lambda tweet: len(tweet))
    return data.groupby("label").mean()["tweet_length"]


def contains_bigram(ngram, adjectives, nouns):
    """Returns the bigrams that match the two regex patterns, adjectives and nouns."""

    bigrams_patterns = [
        rf"""^(?=.*\b{adjective}\b)(?=.*\b{noun}\b).*$"""
        for adjective in adjectives
        for noun in nouns
    ]
    for pattern in bigrams_patterns:
        if re.search(pattern, ngram):
            return ngram

    return None


def count_pejorative_bigrams(bigrams):
    """Returns the pejorative terms and the counts.

    Args:
        bigrams (list of pandas Series) :

    Returns:
        counts (list of tuples) :

    """
    bigrams_counts = [bigrams[i].value_counts() for i in range(0, len(bigrams))]
    counts = []
    for j in range(0, len(bigrams_counts)):
        for i, count in enumerate(bigrams_counts[j]):
            counts.append((bigrams_counts[j].index.values[i], count))

    return counts


#### ALL BELOW REQUIRE SPACY DOCS

def find_most_common_nouns(docs):
    """Returns a descending order sorted list of nouns and their frequencies.

    Args:
        docs (list of spacy docs) : a list of spacy doc obects.

    Return:
        sorted (list of tuples): the word and its count.

    """
    nouns = [str(chunk).strip() for doc in docs for chunk in doc.noun_chunks]

    frequencies = [(word, nouns.count(word)) for word in set(nouns)]

    return sorted(set(frequencies), key=lambda x: x[1], reverse=True)


def part_of_speech_frequency(docs):
    tags = [token.tag_ for doc in docs for token in doc]
    frequencies = [(word, tags.count(word)) for word in set(tags)]
    return sorted(set(frequencies), key=lambda x: x[1], reverse=True)


def spacy_generate_bigrams(docs):
    for doc in docs:
        for noun_phrase in list(doc.noun_chunks):
            noun_phrase.merge(
                noun_phrase.root.tag_,
                noun_phrase.root.lemma_,
                noun_phrase.root.ent_type_,
            )


def load_deptree_into_graph(tweet):
    edges = []
    for token in tweet:
        for child in token.children:
            edges.append((f"{token.lower_}", f"{child.lower_}"))
    return nx.Graph(edges)


def syntactic_dependency_frequency(docs):
    tags = [token.dep_ for doc in docs for token in doc]
    frequencies = [(word, tags.count(word)) for word in set(tags)]
    return sorted(set(frequencies), key=lambda x: x[1], reverse=True)


def compare(function, misogynistic_docs, non_misogynistic_docs):
    misogyny = pd.DataFrame(function(misogynistic_docs),
                            columns=[function.__name__, "count"])
    non_misogyny = pd.DataFrame(
        function(non_misogynistic_docs), columns=[function.__name__, "count"]
    )

    top_10_misogynistic = misogyny.loc[0:10, :]
    top_10_non_misogynistic = non_misogyny.loc[0:10, :]
    return top_10_misogynistic, top_10_non_misogynistic


def verb_noun_syntactic_relation(docs, noun):
    verbs = set()
    for doc in docs:
        for possible_subject in doc:
            if possible_subject.dep == noun and possible_subject.head.pos == VERB:
                verbs.add((possible_subject.text, possible_subject.head))
    return verbs


def verb_noun_word_vectors(docs, noun):
    verb_vectors = np.empty([len(docs), 300])
    verbs = np.chararray((len(docs), 1), unicode=True, itemsize=50)
    nouns = np.chararray((len(docs), 1), unicode=True, itemsize=50)

    for number, doc in enumerate(docs):
        for possible_subject in doc:
            if possible_subject.dep == noun and possible_subject.head.pos == VERB:
                verb_vectors[number, :] = possible_subject.head.vector
                nouns[number, :] = possible_subject.text
                verbs[number, :] = possible_subject.head
    return verb_vectors, verbs, nouns
