import re
import pandas as pd


def density_of_curse_words_in_sentence(tweet):
    """Returns the density of top 20 curse words, taken from Wang, Wenbo,  et  al.  "Cursing  in englishon  twitter."
    The method needs the punctuation to be removed.
    Args:
        tweet (str) : the tweet to be counted.
    Returns:
        density (dict) : the curse words and their densities.
    """
    curse_words = ["fuck", "shit", "ass", "bitch", "nigga", "hell", "whore", "dick", "piss", "pussy", "slut", "puta",
                   "tit", "damn", "fag", "cunt", "cum", "cock", "blowjob"]

    # here we are going to use above words as roots in dictionary and then
    # as dictionary value add them and their plurals in order to make magic happen
    # I'm just adding plural but you can easily extend it with synonyms and such

    curse_roots = {curse_word: [curse_word, f'{curse_word}s'] for curse_word in curse_words}

    # now we create look_up dictionary which is a reverse of above (all values become keys, and key become values)
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

def test_density_of_curse_words_in_sentence():
    tweet = "fuck shit ass bitch nigga hell whore dick piss pussy slut puta tit damn fag cunt cum cock blowjob"
    assert all(density_of_curse_words_in_sentence(tweet))

def test_density_of_curse_words_with_puncuation():
    tweet = "fuck!! fuck, fuck. "
    assert density_of_curse_words_in_sentence(tweet)['fuck'] == 0

def test_density_of_curse_words_with_plurals():
    tweet = "fucks fucks fucks fuck"
    assert density_of_curse_words_in_sentence(tweet)['fuck'] == 1.0

def density_of_curse_words_in_total_corpus(df, dataset_title):
    """Returns density of curse words across an entire corpus

      Args:
        df (pandas df) : the df with the tweets to be counted.

    Returns:
        df (pandas df) : the curse words and their densities.

    """
    df['curse_words'] = df['text'].apply(lambda tweet: density_of_curse_words_in_sentence(tweet))
    count = pd.DataFrame(list(df['curse_words'])).T.sum(axis=1)/len(df)
    return pd.DataFrame({dataset_title: count}, index = count.index)

def generate_ngrams(tweet, n):
    """Returns the n-grams in a sentence.

    Args:
        tweet (str) : the tweet to be grammed.
        n (int) : the number of grams, 2 = bigram, 3 = trigram.

    Returns
        bigrams (list) : a list of bigrams

    """
    tweet = tweet.lower()
    tweet = re.sub(r'[^a-zA-Z0-9\s]', ' ', tweet)

    # Break sentence in the token, remove empty tokens
    tokens = [token for token in tweet.split(" ") if token != ""]

    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

def find_most_common_nouns(docs):
    """Returns a descending order sorted list of nouns and their frequencies.

    Args:
        docs (list of spacy docs) : a list of spacy doc obects.

    Return:
        sorted (list of tuples): the word and its count.

    """
    nouns = [str(chunk) for doc in docs for chunk in doc.noun_chunks]

    frequencies = [(word, nouns.count(word)) for word in set(nouns)]

    return sorted(set(frequencies), key=lambda x: x[1], reverse = True)


def contains_bigram(ngram, adjectives, nouns):
    """Returns the bigrams that match the two regex patterns, adjectives and nouns."""
    match_obj_adjectives = re.search(adjectives, ngram)
    match_obj_nouns = re.search(nouns, ngram)
    try:
        if match_obj_adjectives.group() != "" and match_obj_nouns.group() != "":
            print("Found " + ngram)
            return ngram
    except:
        pass


def count_pejorative_bigrams(bigrams):
    """Returns the pejorative terms and the counts.

    Args:
        bigrams (list of pandas Series) :

    Returns:
        counts (list of tuples) :

    """
    bigrams_counts = [bigrams[i].value_counts() for i in range(0,len(bigrams))]
    counts = []
    for j in range(0,len(bigrams_counts)):
         for i,count in enumerate(bigrams_counts[j]):
            counts.append((bigrams_counts[j].index.values[i], count))

    return counts
