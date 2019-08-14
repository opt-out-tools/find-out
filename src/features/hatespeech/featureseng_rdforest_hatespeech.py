import re

def get_length_of_tweet(tweet):
    """Returns length of tweet."""
    return len(tweet)

MISOGYNY = r"\b(feminazi|sexist|notsexist)"

def contains_misogynstic_vocab(tweet):
    """Returns 1 is the tweet contains the regex MISOGYNY and 0 if not
    Args:
        tweet (str) : The tweet.

    Returns:
        1 or 0 (int)  : The misogyny label.

    """
    return 1 if re.search(MISOGYNY, tweet) else 0
