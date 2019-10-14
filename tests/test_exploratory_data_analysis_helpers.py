import pandas as pd
import spacy

from src.data.preprocess.exploratory_data_analysis_helpers import (
    density_of_curse_words_in_sentence,
)
from src.data.preprocess.exploratory_data_analysis_helpers import find_most_common_nouns
from src.utils.misc import create_spacy_docs
from .utils.domain_objects_test import create_tweets_df

NLP = spacy.load("en_core_web_md")
TWEETS = create_tweets_df()
TWEETS["label"] = pd.Series([1 for _ in range(0, 5)])
DOCS = create_spacy_docs(TWEETS, "text")


def test_find_most_common_nouns():
    nouns = find_most_common_nouns(DOCS)
    assert nouns[0] == ("blocks", 2)


def test_density_of_curse_words_in_sentence():
    tweet = (
        "fuck shit ass bitch nigga hell whore dick piss pussy slut puta tit damn "
        "fag cunt cum cock blowjob"
    )
    assert all(density_of_curse_words_in_sentence(tweet))


def test_density_of_curse_words_with_puncuation():
    tweet = "fuck!! fuck, fuck. "
    assert density_of_curse_words_in_sentence(tweet)["fuck"] == 0


def test_density_of_curse_words_with_plurals():
    tweet = "fucks fucks fucks fuck"
    assert density_of_curse_words_in_sentence(tweet)["fuck"] == 1.0
