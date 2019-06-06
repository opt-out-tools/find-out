import pytest
import pandas as pd
import os
from src.data.preprocess.generate_nn_dataturks import create_dictionary

@pytest.fixture(scope="module")
def read_in_dataset():
    return pd.read_csv(os.getcwd() + "/data/external/dataturks/example.csv")


@pytest.fixture(scope="module")
def create_dataset_vocabulary(read_in_dataset):
    data = read_in_dataset
    return create_dictionary(data['content'], 10000)
