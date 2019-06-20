import pytest
import pandas as pd






@pytest.fixture()
def faulty_df():
    df1 = pd.DataFrame(
        {"A": ["testA" for _ in range(0, 5)], "B": ["testB" for _ in range(0, 5)], "C": ["testC" for _ in range(0, 5)]})
    header_row = pd.DataFrame({"A": ["A"], "B": ["C"], "C": ["B"]})
    df2 = pd.DataFrame(
        {"A": ["testA" for _ in range(0, 5)], "B": ["testC" for _ in range(0, 5)], "C": ["testB" for _ in range(0, 5)]})
    df = pd.concat([df1, header_row, df2])
    return df

def find_header(df, headers):
    for n, row in enumerate(df.iterrows()):
        if row[1].isin(headers).all():
            print(f"Header found at position {n}")
            return n
        else:
            pass

def test_finds_headers(faulty_df):
    assert find_header(faulty_df, ["A", "B", "C"]) != 5 # 0-indexed like skiprows

def write_position_of_headers():
    position_of_headers = []
    df = pd.read_csv("/media/tcake/My Passport/twitter/metoo_tweets.csv", chunksize=100, nrows=10999)
    for chunk in df:
        print(type(chunk))


write_position_of_headers()
