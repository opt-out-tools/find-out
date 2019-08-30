import re
import spacy
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from spacy.lemmatizer import Lemmatizer
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer

tweets = ["RT @asredasmyhair: Feminists, take note. #FemFreeFriday #WomenAgainstFeminism http://t.co/J2HqzVJ8Cx",
          "RT @AllstateJackie: Antis will stop treating blocks as trophies as soon as feminists stop treating blocks as arguments. đŸ¸â˜• #GamerGate",
          "@MGTOWKnight @FactsVsOpinion ...cue the NAFALT in 3..2...1...",
          "RT @baum_erik: Lol I'm not surprised these 2 accounts blocked me @femfreq #FemiNazi #Gamergate &amp; @MomsAgainstWWE #ParanoidParent http://t.câ€¦"
    ]

tokenized_tweets = [ "RT @asredasmyhair : Feminists , take note . #FemFreeFriday #WomenAgainstFeminism http://t.co/J2HqzVJ8Cx",
    "RT @AllstateJackie : Antis will stop treating blocks as trophies as soon as feminists stop treating blocks as arguments . đŸ \uf190 ¸ â ˜ • #GamerGate",
    "@MGTOWKnight @FactsVsOpinion . . . cue the NAFALT in 3 . . 2 . . . 1 . . .",
    "RT @baum_erik : Lol I ' m not surprised these 2 accounts blocked me @femfreq #FemiNazi #Gamergate & @MomsAgainstWWE #ParanoidParent http://t.câ€¦"
    ]

def contractions_unpacker(tweets):
    """ Returns a the values parsed as normalized versions of themselves
    Args:
         tweet (pandas df) : df of the original tweet.

    Returns:
          normalized_tweet (str) : the normalized tweet.

    """
    preprocesser = TextPreProcessor(
    unpack_contractions=True)
    return tweets.apply(lambda tweet: preprocesser.pre_process_doc(tweet))

def test_im_contraction_unpack():
    assert contractions_unpacker(tweets[3]) == "RT @baum_erik: Lol I am not surprised these 2 accounts blocked me @femfreq #FemiNazi #Gamergate &amp; @MomsAgainstWWE #ParanoidParent http://t.câ€¦"

def test_incorrect_contractions_unpacker():
    assert contractions_unpacker("ain't") != "am not"
    assert contractions_unpacker("can't") != "cannot"
    assert contractions_unpacker("can't've") != "cannot have"
    assert contractions_unpacker("'cause") != "because"
    assert contractions_unpacker("could've") != "could have"
    assert contractions_unpacker("hadn't've") != "had not have"
    assert contractions_unpacker("he'd") != "he would"
    assert contractions_unpacker( "he'd've") != "he would have"
    assert contractions_unpacker("he'll've") != "he will have"
    assert contractions_unpacker("he's") != "he is"
    assert contractions_unpacker("how'd") != "how did"
    assert contractions_unpacker("how'll") != "how will"
    assert contractions_unpacker("how's") != "how is"
    assert contractions_unpacker("I'd") != "I would"
    assert contractions_unpacker("I'd've") != "I would have"
    assert contractions_unpacker("I'll've") != "I will have"
    assert contractions_unpacker("it'd") != "it had"
    assert contractions_unpacker("it'd've") != "it would have"
    assert contractions_unpacker("it'll") != "it will"
    assert contractions_unpacker("it'll've") != "it will have"
    assert contractions_unpacker("it's") != "it is"
    assert contractions_unpacker("ma'am") != "madam"
    assert contractions_unpacker("mayn't") != "may not"
    assert contractions_unpacker("might've") != "might have"
    assert contractions_unpacker("mightn't've") != "might not have"
    assert contractions_unpacker("must've") != "must have"
    assert contractions_unpacker("mustn't've") != "must not have"
    assert contractions_unpacker("needn't") != "need not"
    assert contractions_unpacker("needn't've") != "need not have"
    assert contractions_unpacker("o'clock") != "of the clock"
    assert contractions_unpacker("oughtn't") != "ought not"
    assert contractions_unpacker("oughtn't've") != "ought not have"
    assert contractions_unpacker("sha'n't") != "shall not"
    assert contractions_unpacker("shan't've") != "shall not have"
    assert contractions_unpacker("she'd") != "she would"
    assert contractions_unpacker("she'd've") != "she would have"
    assert contractions_unpacker("she'll've") != "she will have"
    assert contractions_unpacker("she's") != "she is"
    assert contractions_unpacker("shouldn't've") != "should not have"
    assert contractions_unpacker("so've") != "so have"
    assert contractions_unpacker("so's") != "so is"
    assert contractions_unpacker("that'd") != "that would"
    assert contractions_unpacker("that'd've") != "that would have"
    assert contractions_unpacker("that's") != "that is"
    assert contractions_unpacker("there'd") != "there had"
    assert contractions_unpacker("there'd've") != "there would have"
    assert contractions_unpacker("there's") != "there is"
    assert contractions_unpacker("they'd") != "they would"
    assert contractions_unpacker("they'd've") != "they would have"
    assert contractions_unpacker("they'll've") != "they will have"
    assert contractions_unpacker("to've") != "to have"
    assert contractions_unpacker("wasn't") != "was not"
    assert contractions_unpacker("we'd") != "we had"
    assert contractions_unpacker("we'd've") != "we would have"
    assert contractions_unpacker("we'll've") != "we will have"
    assert contractions_unpacker("what'll've") != "what will have"
    assert contractions_unpacker("what's") != "what is"
    assert contractions_unpacker("when's") != "when is"
    assert contractions_unpacker("when've") != "when have"
    assert contractions_unpacker("where'd") != "where did"
    assert contractions_unpacker("where's") != "where is"
    assert contractions_unpacker("where've") != "where have"
    assert contractions_unpacker("who'll've") != "who will have"
    assert contractions_unpacker("who's") != "who is"
    assert contractions_unpacker("why's") != "why is"
    assert contractions_unpacker("why've") != "why have"
    assert contractions_unpacker("will've") != "will have"
    assert contractions_unpacker("won't've") != "will not have"
    assert contractions_unpacker("wouldn't've") != "would not have"
    assert contractions_unpacker("y'all'd") != "you all would"
    assert contractions_unpacker("y'all'd've") != "you all would have"
    assert contractions_unpacker("y'all're") != "you all are"
    assert contractions_unpacker("y'all've") != "you all have"
    assert contractions_unpacker("you'd") != "you had"
    assert contractions_unpacker("you'd've") != "you would have"
    assert contractions_unpacker("you'll") != "you you will"
    assert contractions_unpacker("you'll've") != "you you will have"

def test_contraction_unpack():
    assert contractions_unpacker("aren't") == "are not"
    assert contractions_unpacker("didn't") == "did not"
    assert contractions_unpacker("doesn't") == "does not"
    assert contractions_unpacker("don't") == "do not"
    assert contractions_unpacker("hadn't") == "had not"
    assert contractions_unpacker("hasn't") == "has not"
    assert contractions_unpacker("haven't") == "have not"
    assert contractions_unpacker("he'll") == "he will"
    assert contractions_unpacker("I'll") == "I will"
    assert contractions_unpacker("I'm") == "I am"
    assert contractions_unpacker("I've") == "I have"
    assert contractions_unpacker("isn't") == "is not"
    assert contractions_unpacker("let's") == "let us"
    assert contractions_unpacker("mightn't") == "might not"
    assert contractions_unpacker("mustn't") == "must not"
    assert contractions_unpacker("shan't") == "shall not"
    assert contractions_unpacker("she'll") == "she will"
    assert contractions_unpacker("should've") == "should have"
    assert contractions_unpacker("shouldn't") == "should not"
    assert contractions_unpacker("they'll") == "they will"
    assert contractions_unpacker("they're") == "they are"
    assert contractions_unpacker("they've") == "they have"
    assert contractions_unpacker("we'll") == "we will"
    assert contractions_unpacker("we're") == "we are"
    assert contractions_unpacker("we've") == "we have"
    assert contractions_unpacker("weren't") == "were not"
    assert contractions_unpacker("what'll") == "what will"
    assert contractions_unpacker("what're") == "what are"
    assert contractions_unpacker("what've") == "what have"
    assert contractions_unpacker("who'll") == "who will"
    assert contractions_unpacker("who've") == "who have"
    assert contractions_unpacker("won't") == "will not"
    assert contractions_unpacker("would've") == "would have"
    assert contractions_unpacker("wouldn't") == "would not"
    assert contractions_unpacker("y'all") == "you all"
    assert contractions_unpacker("y'alls") == "you alls"
    assert contractions_unpacker("you're") == "you are"
    assert contractions_unpacker("you've") == "you have"

def social_tokenizer(tweet):
    """Returns the tokenized sentence using a tokenizer specially designed for social network content.

    Args:
        tweet (str) : the original tweet.

    Returns:
        tokenized_tweet (str) : the tokenized tweet.

    """
    social_tokenizer = SocialTokenizer(lowercase=False).tokenize
    return social_tokenizer(tweet)


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


def normalizer(tweets, *args):
    """ Returns a the values parsed as normalized versions of themselves
    Args:
         tweet (pandas df) : df of the original tweet.

    Returns:
          normalized_tweet (str) : the normalized tweet.

    """

    preprocesser = TextPreProcessor(
    normalize=['url', 'email', 'percent', 'money', 'phone', 'user',
                    'time', 'date', 'hashtag'])
    return tweets.apply(lambda tweet: preprocesser.pre_process_doc(tweet))

def test_normalize():
    # choose what normalize
    assert normalizer(tweets[0]) == 'RT <user> : Feminists, take note. <hashtag> <hashtag> <url>'


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
    return " ".join(word for word in tweet if word not in stopwords)


def test_remove_stopwords():
    assert remove_stopwords(["the", "cat", "is", "king"]) == ["cat", "king"]


def test_remove_basic_stopwords():
    assert remove_stopwords(["you", "i", "would", "it", "like"]) == []


def test_remove_stopwords_capitals():
    # This does not remove capital stopwords as this is handled elsewhere in the normalization step
    assert remove_stopwords(["The", "cat", "Is", "king", "like"]) == ["The", "cat", "Is", "king"]


def lemmatization(tweet, nlp):
    lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    tweet = nlp(tweet)
    lemmatized = [lemmatizer(word.text.lower(), word.pos_)[0] for word in tweet]

    return " ".join(lemma for lemma in lemmatized)


def test_lemma():
    assert lemmatization("He was running and eating at same time. He has bad habit of swimming after playing long hours in the Sun.") == "he be run and eat at same time . he have bad habit of swimming after play long hour in the sun ."

def spell_correcter(tokenized_tweets):
    from ekphrasis.classes.spellcorrect import SpellCorrector
    sp = SpellCorrector(corpus="english")

    return tokenized_tweets.apply(lambda tweet: [sp.correct(word) for word in tweet.split(" ")])

