import pandas as pd
import re
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from spacy.lemmatizer import Lemmatizer
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer

tweets = ["RT @asredasmyhair: Feminists, take note. #FemFreeFriday #WomenAgainstFeminism http://t.co/J2HqzVJ8Cx",
          "RT @AllstateJackie: Antis will stop treating blocks as trophies as soon as feminists stop treating blocks as arguments. đŸ¸â˜• #GamerGate",
          "@MGTOWKnight @FactsVsOpinion ...cue the NAFALT in 3..2...1...",
          "RT @baum_erik: Lol I'm not surprised these 2 accounts blocked me @femfreq #FemiNazi #Gamergate &amp; @MomsAgainstWWE #ParanoidParent http://t.câ€¦"
    ]
df_tweets = pd.DataFrame({"text": tweets})

tokenized_tweets = [ "RT @asredasmyhair : Feminists , take note . #FemFreeFriday #WomenAgainstFeminism http://t.co/J2HqzVJ8Cx",
    "RT @AllstateJackie : Antis will stop treating blocks as trophies as soon as feminists stop treating blocks as arguments . đŸ \uf190 ¸ â ˜ • #GamerGate",
    "@MGTOWKnight @FactsVsOpinion . . . cue the NAFALT in 3 . . 2 . . . 1 . . .",
    "RT @baum_erik : Lol I ' m not surprised these 2 accounts blocked me @femfreq #FemiNazi #Gamergate & @MomsAgainstWWE #ParanoidParent http://t.câ€¦"
    ]

df_tokenized = pd.DataFrame({"text": tweets})


def contractions_unpacker(tweet):
    """ Returns a the values parsed as normalized versions of themselves
    Args:
         tweet (pandas df) : df of the original tweet.

    Returns:
          normalized_tweet (str) : the normalized tweet.

    """
    contractionsList = {
        "ain't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'd've": "he would have",
        "he'll": "he will",
        "he'll've": "he will have",
        "he's": "he is",
        "how'd": "how did",
        "how'd'y": "how do you",
        "how'll": "how will",
        "how's": "how is",
        "I'd": "I would",
        "I'd've": "I would have",
        "I'll": "I will",
        "I'll've": "I will have",
        "I'm": "I am",
        "I've": "I have",
        "isn't": "is not",
        "it'd": "it had",
        "it'd've": "it would have",
        "it'll": "it will",
        "it'll've": "it will have",
        "it's": "it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "mightn't've": "might not have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "o'clock": "of the clock",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shan't've": "shall not have",
        "she'd": "she would",
        "she'd've": "she would have",
        "she'll": "she will",
        "she'll've": "she will have",
        "she's": "she is",
        "should've": "should have",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "so've": "so have",
        "so's": "so is",
        "that'd": "that would",
        "that'd've": "that would have",
        "that's": "that is",
        "there'd": "there had",
        "there'd've": "there would have",
        "there's": "there is",
        "they'd": "they would",
        "they'd've": "they would have",
        "they'll": "they will",
        "they'll've": "they will have",
        "they're": "they are",
        "they've": "they have",
        "to've": "to have",
        "wasn't": "was not",
        "we'd": "we had",
        "we'd've": "we would have",
        "we'll": "we will",
        "we'll've": "we will have",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what'll've": "what will have",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "when's": "when is",
        "when've": "when have",
        "where'd": "where did",
        "where's": "where is",
        "where've": "where have",
        "who'll": "who will",
        "who'll've": "who will have",
        "who's": "who is",
        "who've": "who have",
        "why's": "why is",
        "why've": "why have",
        "will've": "will have",
        "won't": "will not",
        "won't've": "will not have",
        "would've": "would have",
        "wouldn't": "would not",
        "wouldn't've": "would not have",
        "y'all": "you all",
        "y'alls": "you alls",
        "y'all'd": "you all would",
        "y'all'd've": "you all would have",
        "y'all're": "you all are",
        "y'all've": "you all have",
        "you'd": "you had",
        "you'd've": "you would have",
        "you'll": "you you will",
        "you'll've": "you you will have",
        "you're": "you are",
        "you've": "you have"
    }

    pattern = re.compile(r'\b(?:%s)\b' % '|'.join(contractionsList.keys()))

    def replace(match):
        return contractionsList[match.group(0)]

    return pattern.sub(replace, tweet)

contractionsList = {
        "ain't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'd've": "he would have",
        "he'll": "he will",
        "he'll've": "he will have",
        "he's": "he is",
        "how'd": "how did",
        "how'd'y": "how do you",
        "how'll": "how will",
        "how's": "how is",
        "I'd": "I would",
        "I'd've": "I would have",
        "I'll": "I will",
        "I'll've": "I will have",
        "I'm": "I am",
        "I've": "I have",
        "isn't": "is not",
        "it'd": "it had",
        "it'd've": "it would have",
        "it'll": "it will",
        "it'll've": "it will have",
        "it's": "it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "mightn't've": "might not have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "o'clock": "of the clock",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shan't've": "shall not have",
        "she'd": "she would",
        "she'd've": "she would have",
        "she'll": "she will",
        "she'll've": "she will have",
        "she's": "she is",
        "should've": "should have",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "so've": "so have",
        "so's": "so is",
        "that'd": "that would",
        "that'd've": "that would have",
        "that's": "that is",
        "there'd": "there had",
        "there'd've": "there would have",
        "there's": "there is",
        "they'd": "they would",
        "they'd've": "they would have",
        "they'll": "they will",
        "they'll've": "they will have",
        "they're": "they are",
        "they've": "they have",
        "to've": "to have",
        "wasn't": "was not",
        "we'd": "we had",
        "we'd've": "we would have",
        "we'll": "we will",
        "we'll've": "we will have",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what'll've": "what will have",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "when's": "when is",
        "when've": "when have",
        "where'd": "where did",
        "where's": "where is",
        "where've": "where have",
        "who'll": "who will",
        "who'll've": "who will have",
        "who's": "who is",
        "who've": "who have",
        "why's": "why is",
        "why've": "why have",
        "will've": "will have",
        "won't": "will not",
        "won't've": "will not have",
        "would've": "would have",
        "wouldn't": "would not",
        "wouldn't've": "would not have",
        "y'all": "you all",
        "y'alls": "you alls",
        "y'all'd": "you all would",
        "y'all'd've": "you all would have",
        "y'all're": "you all are",
        "y'all've": "you all have",
        "you'd": "you had",
        "you'd've": "you would have",
        "you'll": "you you will",
        "you'll've": "you you will have",
        "you're": "you are",
        "you've": "you have"
    }

contractions = pd.DataFrame(
        {"contraction": list(contractionsList.keys()), "unpacked": list(contractionsList.values())})

def test_contraction_unpacking():
    contractions['unpacked_values'] = contractions['contraction'].apply(lambda contra: contractions_unpacker(contra))
    assert contractions['unpacked_values'].all() == contractions['unpacked'].all()

def test_im_contraction_unpack():
    df_tweets['contractions'] = df_tweets['text'].apply(lambda tweet: contractions_unpacker(tweet))
    assert df_tweets.loc[3, 'contractions'] == "RT @baum_erik: Lol I am not surprised these 2 accounts blocked me @femfreq #FemiNazi #Gamergate &amp; @MomsAgainstWWE #ParanoidParent http://t.câ€¦"

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
    assert social_tokenizer(tweets[0]) == "RT @asredasmyhair : Feminists , take note . #FemFreeFriday #WomenAgainstFeminism http://t.co/J2HqzVJ8Cx"
    assert social_tokenizer(tweets[1]) == "RT @AllstateJackie : Antis will stop treating blocks as trophies as soon as feminists stop treating blocks as arguments . đŸ \uf190 ¸ â ˜ • #GamerGate"
    assert social_tokenizer(tweets[2]) == "@MGTOWKnight @FactsVsOpinion . . . cue the NAFALT in 3 . . 2 . . . 1 . . ."
    assert social_tokenizer(tweets[3]) == "RT @baum_erik : Lol I ' m not surprised these 2 accounts blocked me @femfreq #FemiNazi #Gamergate & @MomsAgainstWWE #ParanoidParent http://t.câ€¦"

def punctuation_cleaner(tweet):
    """Returns the sentence with punctuation removed. If there is elongated punctuation, this is also removed.

        Args:
            tweet (str) : the original tweet.

        Returns:
            cleaned_tweet (str) : the cleaned tweet.

    """
    # TODO refactor to one line
    return re.sub(r"\s[:,!.](?=\s)?", '', tweet)

def test_removes_colon():
    assert punctuation_cleaner(tokenized_tweets[0]) == "RT @asredasmyhair Feminists take note #FemFreeFriday #WomenAgainstFeminism http://t.co/J2HqzVJ8Cx"

def test_removes_fullstops():
    assert punctuation_cleaner(tokenized_tweets[2]) == "@MGTOWKnight @FactsVsOpinion cue the NAFALT in 3 2 1"

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
    assert lowercase(tokenized_tweets[2]) == "@mgtowknight @factsvsopinion . . . cue the nafalt in 3 . . 2 . . . 1 . . ."


def normalizer(tweets):
    """ Returns a the values parsed as normalized versions of themselves
    Args:
         tweet (pandas df) : df of the original tweet.

    Returns:
          normalized_tweet (str) : the normalized tweet.

    """
    # TODO choose what normalizeS
    preprocesser = TextPreProcessor(
    normalize=['url', 'email', 'percent', 'money', 'phone', 'user',
                    'time', 'date', 'hashtag'])
    return tweets.apply(lambda tweet: preprocesser.pre_process_doc(tweet))

def test_normalize():
    df_tweets['normalized'] = normalizer(df_tweets['text'])
    assert df_tweets.loc[0, 'normalized'] == 'RT <user> : Feminists, take note. <hashtag> <hashtag> <url>'


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



stopwords = ['i', 'like', 'me', 'my', 'im', 'myself', 'we', 'our', 'ours',
       'ourselves', 'you', "you're", 'youre', "you've", 'youve', "you'll",
       'youll', "you'd", 'youd', 'your', 'yours', 'yourself',
       'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's",
       'shes', 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself',
       'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
       'who', 'whom', 'this', 'that', "that'll", 'thatll', 'thats',
       'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
       'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
       'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because',
       'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
       'against', 'between', 'into', 'through', 'during', 'before',
       'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
       'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
       'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
       'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
       'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
       'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'dont',
       'should', "should've", 'shouldve', 'now', 'd', 'll', 'm', 'o',
       're', 've', 'y', 'ain', 'aren', "aren't", 'arent', 'couldn',
       "couldn't", 'couldnt', 'didn', "didn't", 'didnt', 'doesn',
       "doesn't", 'doesnt', 'hadn', "hadn't", 'hadnt', 'hasn', "hasn't",
       'hasnt', 'haven', "haven't", 'havent', 'isn', "isn't", 'isnt',
       'ma', 'mightn', "mightn't", 'mightnt', 'mustn', "mustn't",
       'mustnt', 'needn', "needn't", 'neednt', 'shan', "shan't", 'shant',
       'shouldn', "shouldn't", 'shouldnt', 'wasn', "wasn't", 'wasnt',
       'weren', "weren't", 'werent', 'won', "won't", 'wont', 'wouldn',
       'would', "wouldn't", 'wouldnt']


def remove_stopwords(tweet):
    """Returns a string of words with stop words removed."""
    return " ".join(word for word in tweet.split(" ") if word not in stopwords)


def test_remove_stopwords():
    assert remove_stopwords("the cat is king") == "cat king"


def test_remove_basic_stopwords():
    assert remove_stopwords("you i would it like") == ""


def test_remove_stopwords_capitals():
    # This does not remove capital stopwords as this is handled elsewhere in the normalization step
    assert remove_stopwords("The cat Is king") == "The cat Is king"

# TODO documents and testing
def lemmatization(tweet, nlp):
    lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    tweet = nlp(tweet)
    lemmatized = [lemmatizer(word.text.lower(), word.pos_)[0] for word in tweet]

    return " ".join(lemma for lemma in lemmatized)

def spell_correcter(tokenized_tweets):
    from ekphrasis.classes.spellcorrect import SpellCorrector
    sp = SpellCorrector(corpus="english")

    return tokenized_tweets.apply(lambda tweet: [sp.correct(word) for word in tweet.split(" ")])

