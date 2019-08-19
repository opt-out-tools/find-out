import re


def contains_slut_or_synonyms(tweet):
    """Returns 1 is the tweet contains the substring slut or any synonym and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    SLUT = r"""(slut|whore|tart|tramp|prostitute|hussy|floozy|harlot|hooker|vamp)"""
    return 1 if re.search(SLUT, tweet) else 0


def contains_sexualized_rapeglih_vocab(tweet):
    """Returns 1 is the tweet contains the substring which are sexualized nouns often used in rapeglish and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    RAPEGLISH = r"""(unrapeable slut|cocktease|2hole|two-hole|whore of babylon|cockteaser|slutbag|slag|ladyslut|skank|cum-guzzler|leg-opener|fuck-toy|fuck-toy)"""
    return 1 if re.search(RAPEGLISH, tweet) else 0


def contains_dick_or_synonym(tweet):
    """Returns 1 is the tweet contains the substring dick or it's synonym 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    DICK = r"""\b(dick|cock|chode|fuckpole|knob)"""

    return 1 if re.search(DICK, tweet) else 0


def contains_fuck_whore_same_sentence(tweet):
    """Returns 1 is the tweet contains the substring fuck and whore and 0 if not
     Args:
         tweet (str) : The tweet.
     Returns:
         1 or 0 (int)  : The label.
     """
    verbs = ["rape", "fuck"]
    nouns = ["whore", "women"]
    insults = [rf"""^(?=.*\b{verb}\b)(?=.*\b{noun}\b).*$""" for verb in verbs for noun in nouns]

    for i,insult in enumerate(insults):
        print(f'This is {i} function')
        yield 1 if re.search(insult, tweet) else 0





