import re

from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from spacy.lemmatizer import Lemmatizer

from src.utils.stopwords_and_contractions import stopwords, contractions


def contractions_unpacker(tweet):
    """ Returns the contracted words within the tweet as unpacked
    versions of themselves. eg. she's -> she is

    Args:
         tweet (str) : The original tweet.

    Returns:
          unpacked_tweet (str) : the unpacked tweet.

    """
    contractions_list = contractions()

    pattern = re.compile(
        r"\b(?:%s)\b" % "|".join(contractions_list.keys()), flags=re.IGNORECASE
    )

    def replace(match):
        match = match.group(0).lower()
        return contractions_list[match]

    return pattern.sub(replace, tweet)


def tokenizer(tweet):
    """Returns the tokenized sentence using a tokenizer specially
    designed for social network content, that can handle complex
    emoticons, emojis and other unstructured expressions like dates,
    times and more.

    Args:
        tweet (str) : the original tweet.

    Returns:
        tokenized_tweet (str) : the tokenized tweet.

    """
    social_tokenizer = SocialTokenizer(lowercase=False).tokenize
    return " ".join(s for s in social_tokenizer(tweet))


def punctuation_cleaner(tweet):
    """Returns the sentence with punctuation removed. If there is
    elongated punctuation, this is also removed.

    To be used after the social_tokenizer method.

    Args:
        tweet (str) : the tokenized tweet.

    Returns:
         cleaned_tweet (str) : the cleaned tweet.

    """
    print(tweet)
    return re.sub(r"\s[:,!.](?=\s)?", "", tweet)


def lowercase(tweet):
    """Returns the sentence with all words in lowercase.

     Args:
         tweet (str) : the original tweet.

     Returns:
          lowercase_tweet (str) : the lowercase tweet.

    """
    return " ".join(word.lower() for word in tweet.split())


def normalizer(tweets):
    """ Return a the values parsed as normalized versions of themselves.

    Args:
         tweet (pandas df) : df of the original tweet.

    Returns:
          normalized_tweet (str) : the normalized tweet.

    """
    preprocesser = TextPreProcessor(
        normalize=[
            "url",
            "email",
            "percent",
            "money",
            "phone",
            "user",
            "time",
            "date",
            "hashtag",
        ]
    )
    return tweets.apply(preprocesser.pre_process_doc)


def escape_unicode(tweet):
    """Returns a tokenized tweet where the un-escaped unicode characters
    have been escaped."""
    return [word.encode("utf-8").decode("unicode_escape") for word in tweet]


def replace_spaces(tweet):
    """Replaces the unicode characters for whitespaces and new lines
    with spaces."""
    pattern = "(\\\\xa0)|(\\\\n)|(\\\\xc2)"
    return [
        re.sub(pattern, " ", word) if re.findall(pattern, word) != [] else word
        for word in tweet
    ]


def remove_stopwords(tweet):
    """Returns a string of words with stop words removed."""
    return " ".join(word for word in tweet.split(" ") if word not in stopwords())


def lemmatization(tweet, nlp):
    """Returns the lemma of the tweet."""
    lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    tweet = nlp(tweet)
    lemmatized = [lemmatizer(word.text.lower(), word.pos_)[0] for word in tweet]

    return " ".join(lemma for lemma in lemmatized)


def spell_correcter(tokenized_tweets):
    from ekphrasis.classes.spellcorrect import SpellCorrector

    spell_corrector = SpellCorrector(corpus="english")

    return tokenized_tweets.apply(
        lambda tweet: [spell_corrector.correct(word) for word in tweet.split(" ")]
    )
