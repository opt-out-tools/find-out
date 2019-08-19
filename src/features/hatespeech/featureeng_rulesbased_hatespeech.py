import re
import numpy as np

SLUT = r"slut|whore|tart|tramp|prostitute|hussy|floozy|harlot|hooker|vamp"

def contains_slut_or_synonyms(tweet):
    """Returns 1 is the tweet contains the substring slut or any synonym and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The misogyny label.
    """
    return 1 if re.search(SLUT, tweet) else 0

RAPEGLISH = r"unrapeable slut|cocktease|2hole|two-hole|whore of babylon|cockteaser|slutbag|slag|ladyslut|skank|cum-guzzler|leg-opener|fuck-toy|fuck-toy"

def contains_sexualized_rapeglih_vocab(tweet):
    """Returns 1 is the tweet contains the substring which are sexualized nouns often used in rapeglish and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The misogyny label.
    """
    return 1 if re.search(RAPEGLISH, tweet) else 0



def combine_feature_space(wordvecs, feature_to_add):
    """Returns 1 is the tweet contains the substring which are sexualized nouns often used in rapeglish and 0 if not
    Args:
        wordvectors (csr_matrix) : The tf-idf word vectors
        feature_to_add (np array : The new feature to add.
    Returns:
        combined feature space (np array)  : The combined tf-idf and feature space.
    """
    wordvecs = wordvecs.toarray()
    feature_to_add = feature_to_add.reshape(len(wordvecs), 1)
    return np.hstack((wordvecs,feature_to_add))
