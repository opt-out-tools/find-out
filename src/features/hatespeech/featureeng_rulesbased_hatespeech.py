import re

ABSTAIN = 0
POSITIVE = 1
NEGATIVE = 2


def contains_slut_or_synonyms(tweet):
    """Returns 1 is the tweet contains the substring slut or any synonym and
    0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    slut = r"""(slut|whore|tart|tramp|prostitute|hussy|floozy|harlot|hooker
    |vamp|slag|skank)"""
    return POSITIVE if re.search(slut, tweet) else ABSTAIN


def contains_cunt_or_synonyms(tweet):
    """Returns 1 is the tweet contains the substring cunt or any synonym and
    0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    cunt = r"""(cunt|slit|pussy|fanny|twat|snatch|vagina)"""
    return POSITIVE if re.search(cunt, tweet) else ABSTAIN


def contains_dyke_or_synonyms(tweet):
    """Returns 1 is the tweet contains the substring dyke or any synonym and
    0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    dyke = r"""(dyke|lesbian|butch|dike)"""
    return POSITIVE if re.search(dyke, tweet) else ABSTAIN


def contains_camel_toe(tweet):
    """Returns 1 is the tweet contains the substring cunt or any synonym and
    0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    camel_toe = r"""camel toe"""
    return POSITIVE if re.search(camel_toe, tweet) else ABSTAIN


def contains_feminazi(tweet):
    """Returns 1 is the tweet contains the substring not sexist but or any
    synonym and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    feminazi = r"""feminazi"""
    return POSITIVE if re.search(feminazi, tweet) else ABSTAIN


def contains_not_sexist(tweet):
    """Returns 1 is the tweet contains the substring not sexist but or any
    synonym and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    not_sexist = r"""not sexist"""
    return POSITIVE if re.search(not_sexist, tweet) else ABSTAIN


def contains_not_sexist_hashtag(tweet):
    """Returns 1 is the tweet contains the substring notsexist hashtag but
    or any synonym and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    not_sexist_hashtag = r"""notsexist"""
    return POSITIVE if re.search(not_sexist_hashtag, tweet) else ABSTAIN


def contains_sexualized_rapeglih_vocab(tweet):
    """Returns 1 is the tweet contains the substring which are sexualized
    nouns often used in rapeglish and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    rapeglish = r"""(unrapeable slut|cocktease|2hole|two-hole|whore of 
    babylon|cockteaser|slutbag|slag|ladyslut|skank|cum-guzzler|leg-opener
    |fuck-toy|fuck-toy|carpet muncher)"""
    return POSITIVE if re.search(rapeglish, tweet) else ABSTAIN


def contains_dick_or_synonym(tweet):
    """Returns 1 is the tweet contains the substring dick or it's synonym 0
    if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    dick = r"""(dick|cock|chode|fuckpole|knob|choad)"""

    return POSITIVE if re.search(dick, tweet) else ABSTAIN


def contains_bitch_cunt(tweet):
    """Returns 1 is the tweet contains the substring or combinations of that
    are insultive and 0 if not
    Args:
        tweet (str) : The tweet.
    Returns:
        1 or 0 (int)  : The label.
    """
    adjectives = ["dumb", "fucking", "stupid", "greedy", "fuck", "dumbest",
                  "lying"]
    nouns = ["bitch", "cunt", "whore"]
    insults = [rf"""^(?=.*\b{adjective}\b)(?=.*\b{noun}\b).*$""" for adjective
               in adjectives for noun in nouns]

    ABSTAIN = 0
    POSITIVE = 1

    for insult in insults:
        yield POSITIVE if re.search(insult, tweet) else ABSTAIN, insult


def contains_fuck_whore_same_sentence(tweet):
    """Returns 1 is the tweet contains the substring fuck and whore and 0 if
    not
     Args:
         tweet (str) : The tweet.
     Returns:
         1 or 0 (int)  : The label.
     """
    verbs = ["rape", "fuck"]
    nouns = ["whore", "women", "slut", "girl"]
    insults = [rf"""^(?=.*\b{verb}\b)(?=.*\b{noun}\b).*$""" for verb in verbs
               for noun in nouns]

    abstain = 0
    positive = 1

    for i, insult in enumerate(insults):
        yield positive if re.search(insult, tweet) else abstain, insult


def contains_women_stereotypes(tweet):
    """Returns 1 is the tweet contains the substring women can't drive and 0
    if not
     Args:
         tweet (str) : The tweet.
     Returns:
         1 or 0 (int)  : The label.
     """
    negation = ["cant", "cannot", "shouldnt"]
    nouns = ["whores?", "women", "sluts?", "girls?", "bitches?"]
    actions = ["drive", "ref", "be president", "be in politics",
               "be a politician", "play sports", "do maths"]

    insults = [rf"""^(?=.*\b{noun}\b)(?=.*\b{negate}\b)(?=.* \b{act}\b).*$"""
               for act in actions for negate in negation
               for noun in nouns]

    abstain = 0
    positive = 1

    for insult in insults:
        yield positive if re.search(insult, tweet) else abstain, insult
