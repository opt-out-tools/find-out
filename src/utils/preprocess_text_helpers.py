import pandas as pd
import re
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from spacy.lemmatizer import Lemmatizer
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer

from src.utils.stopwords_and_contractions import stopwords, contractions
from src.utils.domain_objects_test import create_tweets_df, create_tokenized_tweets_df

def contractions_unpacker(tweet):
    """ Returns the contracted words within the tweet as unpacked versions of themselves. eg. she's -> she is

    Args:
         tweet (str) : The original tweet.

    Returns:
          unpacked_tweet (str) : the unpacked tweet.

    """
    contractionsList = contractions()

    pattern = re.compile(r'\b(?:%s)\b' % '|'.join(contractionsList.keys()), flags=re.IGNORECASE)

    def replace(match):
        match = match.group(0).lower()
        return contractionsList[match]

    return pattern.sub(replace, tweet)

tweets = create_tweets_df()
tokenized_tweets = create_tokenized_tweets_df()

df_contractions = pd.DataFrame(
        {"contraction": list(contractions().keys()), "unpacked": list(contractions().values())})

def test_contraction_unpacking_all():
    df_contractions['unpacked_values'] = df_contractions['contraction'].apply(lambda contra: contractions_unpacker(contra))
    assert df_contractions['unpacked_values'].all() == df_contractions['unpacked'].all()

def test_contraction_unpack_in_sentence():
    tweets['contractions'] = tweets['text'].apply(lambda tweet: contractions_unpacker(tweet))
    assert tweets.loc[3, 'contractions'] == "RT @baum_erik: Lol I am not surprised these 2 accounts blocked me @femfreq #FemiNazi #Gamergate &amp; @MomsAgainstWWE #ParanoidParent http://t.câ€¦"

def test_contraction_unpack_case_agnostic():
    assert contractions_unpacker("Ain't") == "am not"
    assert contractions_unpacker("I'm") == "I am"

def social_tokenizer(tweet):
    """Returns the tokenized sentence using a tokenizer specially designed for social network content.

    Args:
        tweet (str) : the original tweet.

    Returns:
        tokenized_tweet (str) : the tokenized tweet.

    """
    social_tokenizer = SocialTokenizer(lowercase=False).tokenize
    return " ".join(s for s in social_tokenizer(tweet))


def test_social_tokenizer():
    # TODO how to handle invalid unicode or leave it and use it as feature because indication of obfuscation
    assert social_tokenizer(tweets.loc[0, 'text']) == "RT @asredasmyhair : Feminists , take note . #FemFreeFriday #WomenAgainstFeminism http://t.co/J2HqzVJ8Cx"
    assert social_tokenizer(tweets.loc[1, 'text']) == "RT @AllstateJackie : Antis will stop treating blocks as trophies as soon as feminists stop treating blocks as arguments . đŸ \uf190 ¸ â ˜ • #GamerGate"
    assert social_tokenizer(tweets.loc[2, 'text']) == "@MGTOWKnight @FactsVsOpinion . . . cue the NAFALT in 3 . . 2 . . . 1 . . ."
    assert social_tokenizer(tweets.loc[3, 'text']) == "RT @baum_erik : Lol I ' m not surprised these 2 accounts blocked me @femfreq #FemiNazi #Gamergate & @MomsAgainstWWE #ParanoidParent http://t.câ€¦"

def punctuation_cleaner(tweet):
    """Returns the sentence with punctuation removed. If there is elongated punctuation, this is also removed.

    Args:
        tweet (str) : the original tweet.

    Returns:
         cleaned_tweet (str) : the cleaned tweet.

    """
    return re.sub(r"\s[:,!.](?=\s)?", '', tweet)

def test_removes_colon():
    assert punctuation_cleaner(tokenized_tweets.loc[0, 'text']) == "RT @asredasmyhair Feminists take note #FemFreeFriday #WomenAgainstFeminism http://t.co/J2HqzVJ8Cx"

def test_removes_fullstops():
    assert punctuation_cleaner(tokenized_tweets.loc[2, 'text']) == "@MGTOWKnight @FactsVsOpinion cue the NAFALT in 3 2 1"

def test_removes_exclamation_marks():
    tweet = "@MGTOWKnight @FactsVsOpinion . . . cue the NAFALT in 3 . . 2 . . . 1 ! ! !"
    assert punctuation_cleaner(tweet) == "@MGTOWKnight @FactsVsOpinion cue the NAFALT in 3 2 1"

def lowercase(tweet):
    """Returns the sentence with all words in lowercase.

     Args:
         tweet (str) : the original tweet.

     Returns:
          lowercase_tweet (str) : the lowercase tweet.

    """
    return " ".join(word.lower() for word in tweet.split())


def test_lowercase():
    assert lowercase(tokenized_tweets.loc[2, 'text']) == "@mgtowknight @factsvsopinion . . . cue the nafalt in 3 . . 2 . . . 1 . . ."


def normalizer(tweets):
    """ Returns a the values parsed as normalized versions of themselves.

    Args:
         tweet (pandas df) : df of the original tweet.

    Returns:
          normalized_tweet (str) : the normalized tweet.

    """
    # TODO choose what normalize
    preprocesser = TextPreProcessor(
    normalize=['url', 'email', 'percent', 'money', 'phone', 'user',
                    'time', 'date', 'hashtag'])
    return tweets.apply(lambda tweet: preprocesser.pre_process_doc(tweet))

def test_normalize():
    tweets['normalized'] = normalizer(tweets['text'])
    assert tweets.loc[0, 'normalized'] == 'RT <user> : Feminists, take note. <hashtag> <hashtag> <url>'


def escape_unicode(tweet):
    """Returns a tokenized tweet where the un-escaped unicode characters have been escaped."""
    return [word.encode('utf-8').decode('unicode_escape') if re.findall('\\\\\w+', word) != [] else word for word in
            tweet]

def test_escape_a_acute():
    assert escape_unicode(['\\xe1']) == ['á']


def test_escape_a_umlaut():
    assert escape_unicode(['\\xe4']) == ['ä']


def test_escape_inverted_question_mark():
    assert escape_unicode(['\\xbf']) == ['¿']


def test_escape_sentence():
    assert escape_unicode(['Iam\\xbf trying to \\xe4figure out \\xe1 unicode']) == [
        'Iam¿ trying to äfigure out á unicode']


def replace_spaces(tweet):
    """Replaces the unicode characters for whitespaces and new lines with spaces."""
    pattern = '(\\\\xa0)|(\\\\n)|(\\\\xc2)'
    return [re.sub(pattern, " ", word) if re.findall(pattern, word) != [] else word for word in tweet]


def test_replace_whitespace():
    assert replace_spaces(['\\ntest']) == [' test']


def test_replace_beginning():
    assert replace_spaces(['\\xa0test test']) == [' test test']


def test_replace_middle():
    assert replace_spaces(['test\\xa0test']) == ['test test']


def test_replace_middle_twice():
    assert replace_spaces(['test\\xa0\\xa0test']) == ['test  test']


def test_replace_end():
    assert replace_spaces(['test\\xa0']) == ['test ']


def test_replace_space():
    assert replace_spaces(['test\\n test']) == ['test  test']


def test_replace_two_times():
    assert replace_spaces(['test\\n test\\n test']) == ['test  test  test']


def test_replace_different_unicode():
    assert replace_spaces(['test\\xc2\\xa0test\\ntest']) == ['test  test test']


def remove_stopwords(tweet):
    """Returns a string of words with stop words removed."""
    return " ".join(word for word in tweet.split(" ") if word not in stopwords())


def test_remove_stopwords():
    assert remove_stopwords("the cat is king") == "cat king"


def test_remove_basic_stopwords():
    assert remove_stopwords("you i would it like") == ""


def test_remove_stopwords_capitals():
    # This does not remove capital stopwords as this is handled elsewhere in the normalization step
    assert remove_stopwords("The cat Is king") == "The cat Is king"

# TODO documents and testing
def lemmatization(tweet, nlp):
    """Returns the lemma of the tweet."""
    lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    tweet = nlp(tweet)
    lemmatized = [lemmatizer(word.text.lower(), word.pos_)[0] for word in tweet]

    return " ".join(lemma for lemma in lemmatized)

# TODO spell correct performs slow and poorly, need to investigate
def spell_correcter(tokenized_tweets):

    from ekphrasis.classes.spellcorrect import SpellCorrector
    sp = SpellCorrector(corpus="english")

    return tokenized_tweets.apply(lambda tweet: [sp.correct(word) for word in tweet.split(" ")])

# suggested order
# data['contractions_unpacked'] = data['text'].apply(lambda tweet: contractions_unpacker(tweet))
# data['tokenize'] = data['contractions_unpacked'].apply(lambda tweet: social_tokenizer(tweet))
# data['remove_punctuation'] = data['tokenize'].apply(lambda tweet: punctuation_cleaner(tweet))
# data['remove_stopwords'] = data['remove_punctuation'].apply(lambda tweet: remove_stopwords(tweet))
# data['norm_removed_stopwords'] = normalizer(data['remove_stopwords'])

