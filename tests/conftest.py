import pandas as pd
import pytest

from src.data.preprocess.dataturks.generate_nn_dataturks import create_dictionary
from src.utils.misc import create_spacy_docs
from tests.test_data.tweet_objects import create_tweets_df
from tests.test_data.tweet_objects import create_tweets_with_labels_df


@pytest.fixture(scope="module")
def create_dataset_vocabulary():
    data = pd.read_csv("../data/external/dataturks/example.csv")
    return create_dictionary(data["content"], 10000)

@pytest.fixture
def tweets():
    return create_tweets_df()

@pytest.fixture
def spacy_docs():
    return create_spacy_docs(create_tweets_with_labels_df(), "text")


