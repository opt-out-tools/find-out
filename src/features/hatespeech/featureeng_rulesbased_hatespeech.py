import re


ABSTAIN = 0
POSITIVE = 1
NEGATIVE = 2

def contains_slut_or_synonyms(tweet):
    """Returns 1 is the tweet contains the substring slut or any synonym and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    SLUT = r"""(slut|whore|tart|tramp|prostitute|hussy|floozy|harlot|hooker|vamp|slag|skank)"""
    return POSITIVE if re.search(SLUT, tweet) else ABSTAIN

def contains_cunt_or_synonyms(tweet):
    """Returns 1 is the tweet contains the substring cunt or any synonym and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    CUNT = r"""(cunt|slit|pussy|fanny|twat|snatch|)"""
    return POSITIVE if re.search(CUNT, tweet) else ABSTAIN

def contains_feminazi(tweet):
    """Returns 1 is the tweet contains the substring not sexist but or any synonym and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    FEMINAZI = r"""feminazi"""
    return POSITIVE if re.search(FEMINAZI, tweet) else ABSTAIN

def contains_not_sexist(tweet):
    """Returns 1 is the tweet contains the substring not sexist but or any synonym and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    NOT_SEXIST = r"""not sexist"""
    return POSITIVE if re.search(NOT_SEXIST, tweet) else ABSTAIN

def contains_not_sexist_hashtag(tweet):
    """Returns 1 is the tweet contains the substring notsexist hashtag but or any synonym and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    NOT_SEXIST_HASHTAG = r"""notsexist"""
    return POSITIVE if re.search(NOT_SEXIST_HASHTAG, tweet) else ABSTAIN

def contains_sexualized_rapeglih_vocab(tweet):
    """Returns 1 is the tweet contains the substring which are sexualized nouns often used in rapeglish and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    RAPEGLISH = r"""(unrapeable slut|cocktease|2hole|two-hole|whore of babylon|cockteaser|slutbag|slag|ladyslut|skank|cum-guzzler|leg-opener|fuck-toy|fuck-toy|carpet muncher)"""
    return POSITIVE if re.search(RAPEGLISH, tweet) else ABSTAIN


def contains_dick_or_synonym(tweet):
    """Returns 1 is the tweet contains the substring dick or it's synonym 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    DICK = r"""\b(dick|cock|chode|fuckpole|knob|choad)"""

    return POSITIVE if re.search(DICK, tweet) else ABSTAIN

def contains_bitch(tweet):
    """Returns 1 is the tweet contains the substring or combinations of that are insultive and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    adjectives = ["dumb", "fucking", "stupid", "greedy", "fuck", "dumbest"]
    nouns = ["bitch", "cunt"]
    insults = [rf"""^(?=.*\b{adjective}\b)(?=.*\b{noun}\b).*$""" for adjective in adjectives for noun in nouns]

    ABSTAIN = 0
    POSITIVE = 1

    for i, insult in enumerate(insults):
        yield POSITIVE if re.search(insult, tweet) else ABSTAIN, insult


def contains_fuck_whore_same_sentence(tweet):
    """Returns 1 is the tweet contains the substring fuck and whore and 0 if not
     Args:
         tweet (str) : The tweet.
     Returns:
         1 or 0 (int)  : The label.
     """
    verbs = ["rape", "fuck"]
    nouns = ["whore", "women", "slut", "girl"]
    insults = [rf"""^(?=.*\b{verb}\b)(?=.*\b{noun}\b).*$""" for verb in verbs for noun in nouns]

    ABSTAIN = 0
    POSITIVE = 1

    for i,insult in enumerate(insults):
        yield POSITIVE if re.search(insult, tweet) else ABSTAIN, insult

def contains_women_bad_drivers(tweet):
    """Returns 1 is the tweet contains the substring women can't drive and 0 if not
     Args:
         tweet (str) : The tweet.
     Returns:
         1 or 0 (int)  : The label.
     """
    negation = ["cant", "cannot","shouldnt"]
    nouns = ["whores?", "women", "sluts?", "girls?", "bitches?"]
    verbs = ["drive","ref", "be president", "be in politics", "be a politician"]

    insults = [rf"""^(?=.*\b{noun}\b)(?=.*\b{negate}\b)(?=.* \b{verb}\b).*$""" for verb in verbs for negate in negation for noun in nouns]

    ABSTAIN = 0
    POSITIVE = 1

    for i,insult in enumerate(insults):
        yield POSITIVE if re.search(insult, tweet) else ABSTAIN, insult






