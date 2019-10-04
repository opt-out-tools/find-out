import pandas as pd


def create_tweets_df():
    tweets = [
        "RT @asredasmyhair: Feminists, take note. #FemFreeFriday "
        "#WomenAgainstFeminism http://t.co/J2HqzVJ8Cx",
        "RT @AllstateJackie: Antis will stop treating blocks as trophies as "
        "soon as feminists stop treating blocks as arguments. đŸ¸â˜• "
        "#GamerGate",
        "@MGTOWKnight @FactsVsOpinion ...cue the NAFALT in 3..2...1...",
        "RT @baum_erik: Lol I'm not surprised these 2 accounts blocked me "
        "@femfreq #FemiNazi #Gamergate &amp; @MomsAgainstWWE #ParanoidParent "
        "http://t.câ€¦",
    ]
    return pd.DataFrame({"text": tweets})


def create_tokenized_tweets_df():
    tokenized_tweets = [
        "RT @asredasmyhair : Feminists , take note . #FemFreeFriday "
        "#WomenAgainstFeminism http://t.co/J2HqzVJ8Cx",
        "RT @AllstateJackie : Antis will stop treating blocks as trophies as "
        "soon as feminists stop treating blocks as arguments . đŸ \uf190 ¸ â "
        "˜ • #GamerGate",
        "@MGTOWKnight @FactsVsOpinion . . . cue the NAFALT in 3 . . 2 . . . "
        ""
        "1 . . .",
        "RT @baum_erik : Lol I ' m not surprised these 2 accounts blocked me "
        "@femfreq #FemiNazi #Gamergate & @MomsAgainstWWE #ParanoidParent "
        "http://t.câ€¦",
    ]

    return pd.DataFrame({"text": tokenized_tweets})


def create_tweets_with_labels_df():
    tweets = [
        "RT @asredasmyhair: Feminists, take note. #FemFreeFriday "
        "#WomenAgainstFeminism http://t.co/J2HqzVJ8Cx",
        "RT @AllstateJackie: Antis will stop treating blocks as trophies as "
        "soon as feminists stop treating blocks as arguments. đŸ¸â˜• "
        "#GamerGate",
        "@MGTOWKnight @FactsVsOpinion ...cue the NAFALT in 3..2...1...",
        "RT @baum_erik: Lol I'm not surprised these 2 accounts blocked me "
        "@femfreq #FemiNazi #Gamergate &amp; @MomsAgainstWWE #ParanoidParent "
        "http://t.câ€¦",
    ]
    return pd.DataFrame(
        {
            "text": tweets,
            "label": pd.Series([1 if number % 2 == 0 else 0 for number in range(0, 4)]),
        }
    )
