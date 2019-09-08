from src.utils.preprocess_text_pipelines import normalize, clean, tokenize
from src.utils.domain_objects_test import create_tweets_df

TWEETS = create_tweets_df()


def test_normalize():
    assert (
        normalize(TWEETS).loc[0, "normalized"]
        == "RT <user> Feminists take note <hashtag> "
        "<hashtag> <url>"
    )
    assert (
        normalize(TWEETS).loc[1, "normalized"]
        == "RT <user> Antis stop treating blocks "
        "trophies soon feminists stop treating "
        "blocks arguments đŸ \uf190 ¸ â ˜ • "
        "<hashtag>"
    )
    assert normalize(TWEETS).loc[2, "normalized"] == "<user> <user> cue NAFALT 3 2 1"
    assert (
        normalize(TWEETS).loc[3, "normalized"]
        == "RT <user> Lol I surprised 2 accounts "
        "blocked <user> <hashtag> <hashtag> & "
        "<user> <hashtag> <url>"
    )


def test_clean():
    assert (
        clean(TWEETS).loc[0, "cleaned"] == "RT @asredasmyhair Feminists take note "
        "#FemFreeFriday #WomenAgainstFeminism "
        "http://t.co/J2HqzVJ8Cx"
    )
    assert (
        clean(TWEETS).loc[1, "cleaned"] == "RT @AllstateJackie Antis stop treating "
        "blocks trophies soon feminists stop "
        "treating blocks arguments đŸ \uf190 ¸ â ˜ • "
        ""
        "#GamerGate"
    )
    assert (
        clean(TWEETS).loc[2, "cleaned"]
        == "@MGTOWKnight @FactsVsOpinion cue NAFALT 3 2 1"
    )
    assert (
        clean(TWEETS).loc[3, "cleaned"] == "RT @baum_erik Lol I surprised 2 accounts "
        "blocked @femfreq #FemiNazi #Gamergate & "
        "@MomsAgainstWWE #ParanoidParent "
        "http://t.câ€¦"
    )


def test_tokenize():
    assert (
        tokenize(TWEETS).loc[0, "tokenized"]
        == "RT @asredasmyhair : Feminists , take note "
        ""
        ". #FemFreeFriday #WomenAgainstFeminism "
        "http://t.co/J2HqzVJ8Cx"
    )
    assert (
        tokenize(TWEETS).loc[1, "tokenized"] == "RT @AllstateJackie : Antis will stop "
        "treating blocks as trophies as soon as "
        "feminists stop treating blocks as "
        "arguments . đŸ \uf190 ¸ â ˜ • #GamerGate"
    )
    assert (
        tokenize(TWEETS).loc[2, "tokenized"]
        == "@MGTOWKnight @FactsVsOpinion . . . cue "
        "the NAFALT in 3 . . 2 . . . 1 . . ."
    )
    assert (
        tokenize(TWEETS).loc[3, "tokenized"]
        == "RT @baum_erik : Lol I am not surprised "
        "these 2 accounts blocked me @femfreq "
        "#FemiNazi #Gamergate & @MomsAgainstWWE "
        "#ParanoidParent http://t.câ€¦"
    )
