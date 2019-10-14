import pandas as pd
import pytest

from src.data.preprocess.dataturks.generate_nn_dataturks import create_dictionary


@pytest.fixture(scope="module")
def create_dataset_vocabulary():
    data = pd.read_csv("data/external/dataturks/example.csv")
    return create_dictionary(data["content"], 10000)
