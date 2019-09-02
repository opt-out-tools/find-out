from src.utils.domain_objects_test import create_tweets_df, create_tokenized_tweets_df
from src.utils.preprocess_text_helpers import contractions_unpacker, social_tokenizer, remove_stopwords, normalizer, \
    punctuation_cleaner

tweets = create_tweets_df()

def normalize(df):
    """Returns normalized text.

    Args
        df (pandas df) : the dataframe with the tweets under a column labeled text.

    Returns
        df (pandas df) : the normalized tweets under the column normalized.

    """
    df['normalized'] = df['text'].apply(lambda tweet: contractions_unpacker(tweet))
    df['normalized'] = df['normalized'].apply(lambda tweet: social_tokenizer(tweet))
    df['normalized'] = df['normalized'].apply(lambda tweet: punctuation_cleaner(tweet))
    df['normalized'] = df['normalized'].apply(lambda tweet: remove_stopwords(tweet))
    df['normalized'] = normalizer(df['normalized'])
    return df

def test_normalize():
    assert normalize(tweets).loc[0,'normalized'] == "RT <user> Feminists take note <hashtag> <hashtag> <url>"
    assert normalize(tweets).loc[1, 'normalized'] == "RT <user> Antis stop treating blocks trophies soon feminists stop treating blocks arguments đŸ \uf190 ¸ â ˜ • <hashtag>"
    assert normalize(tweets).loc[2, 'normalized'] == "<user> <user> cue NAFALT 3 2 1"
    assert normalize(tweets).loc[3, 'normalized'] == "RT <user> Lol I surprised 2 accounts blocked <user> <hashtag> <hashtag> & <user> <hashtag> <url>"

def clean(df):
    """Returns cleaned text.

       Args
           df (pandas df) : the dataframe with the tweets under a column labeled text.

       Returns
           df (pandas df) : the cleaned tweets under the column cleaned.

    """
    df['cleaned'] = df['text'].apply(lambda tweet: contractions_unpacker(tweet))
    df['cleaned'] = df['cleaned'].apply(lambda tweet: social_tokenizer(tweet))
    df['cleaned'] = df['cleaned'].apply(lambda tweet: punctuation_cleaner(tweet))
    df['cleaned'] = df['cleaned'].apply(lambda tweet: remove_stopwords(tweet))
    return df

def test_clean():
    assert clean(tweets).loc[0,'cleaned'] == "RT @asredasmyhair Feminists take note #FemFreeFriday #WomenAgainstFeminism http://t.co/J2HqzVJ8Cx"
    assert clean(tweets).loc[1, 'cleaned'] == "RT @AllstateJackie Antis stop treating blocks trophies soon feminists stop treating blocks arguments đŸ \uf190 ¸ â ˜ • #GamerGate"
    assert clean(tweets).loc[2, 'cleaned'] == "@MGTOWKnight @FactsVsOpinion cue NAFALT 3 2 1"
    assert clean(tweets).loc[3, 'cleaned'] == "RT @baum_erik Lol I surprised 2 accounts blocked @femfreq #FemiNazi #Gamergate & @MomsAgainstWWE #ParanoidParent http://t.câ€¦"

def tokenize(df):
    """Returns tokenized text in string format.

       Args
           df (pandas df) : the dataframe with the tweets under a column labeled text.

       Returns
           df (pandas df) : the tokenized tweets under the column tokenized.

    """
    df['tokenized'] = df['text'].apply(lambda tweet: contractions_unpacker(tweet))
    df['tokenized'] = df['tokenized'].apply(lambda tweet: social_tokenizer(tweet))
    return df

def test_tokenize():
    assert tokenize(tweets).loc[0,'tokenized'] == "RT @asredasmyhair : Feminists , take note . #FemFreeFriday #WomenAgainstFeminism http://t.co/J2HqzVJ8Cx"
    assert tokenize(tweets).loc[1, 'tokenized'] == "RT @AllstateJackie : Antis will stop treating blocks as trophies as soon as feminists stop treating blocks as arguments . đŸ \uf190 ¸ â ˜ • #GamerGate"
    assert tokenize(tweets).loc[2, 'tokenized'] == "@MGTOWKnight @FactsVsOpinion . . . cue the NAFALT in 3 . . 2 . . . 1 . . ."
    assert tokenize(tweets).loc[3, 'tokenized'] == "RT @baum_erik : Lol I am not surprised these 2 accounts blocked me @femfreq #FemiNazi #Gamergate & @MomsAgainstWWE #ParanoidParent http://t.câ€¦"
