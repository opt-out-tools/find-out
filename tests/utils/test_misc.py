import spacy

from src.utils.misc import create_spacy_docs
from .domain_objects_test import create_tweets_with_labels_df

NLP = spacy.load("en_core_web_md")
TWEETS = create_tweets_with_labels_df()


def test_create_spacy_docs_misogynistic():
    docs = create_spacy_docs(TWEETS, "text")
    assert len(docs) == 4
