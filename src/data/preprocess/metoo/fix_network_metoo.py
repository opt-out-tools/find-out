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

def find_header(df, headers, positions):
    for n, row in enumerate(df.iterrows()):
        if row[1].isin(headers).any():
            print(f"Header found at position {n}")
            positions.append(n)
        else:
            pass
    return positions

def test_finds_headers(faulty_df):
    positions = []
    assert find_header(faulty_df, ["A", "B", "C"], positions) == [5] # 0-indexed like skiprows

def write_position_of_headers():
    position_of_headers = [0]
    headers =  ['contributors']
    df = pd.read_csv("/home/tcake/coding_projects/python/opt_out/metoo_tweets.csv")
    find_header(df, headers, position_of_headers)

    return position_of_headers



positions = write_position_of_headers()
import numpy as np

npa = np.asarray(positions, dtype=np.int32)

np.savetxt("header_position.txt", npa, fmt='%d')

# Initialize collective df
df_total = pd.read_csv("/home/tcake/coding_projects/python/opt_out/metoo_tweets.csv", skiprows= 0, nrows=61, header=0)
# For each found header, save to dataframe and concat with initial
for i in range(1, len(npa)-1):
    skip = npa[i]
    nrow = npa[i + 1] - npa[i]
    df = pd.read_csv("/home/tcake/coding_projects/python/opt_out/metoo_tweets.csv", skiprows=skip + 1, nrows=nrow - 1,
                     header=0) # stops before so need to add one and -1 to make up for that
    df_total = pd.concat([df_total, df.iloc[:,1:]])
df_total.to_csv("/home/tcake/coding_projects/python/opt_out/fixed_metoo_tweets.csv")
