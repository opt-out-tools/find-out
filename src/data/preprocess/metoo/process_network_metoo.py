import ast

import pandas as pd


def create_df(df):
    entity = df.fillna("{}")

    entity = entity.apply(ast.literal_eval)

    tmp = entity.values.tolist()

    entity = pd.DataFrame(tmp)

    return entity


if __name__ == "__main__":
    df = pd.read_csv("../../../../data/interim/sample_metoo_tweets.csv")
    users = create_df(df["user"])
    entities = create_df(df["entities"])
    retweets = create_df(df["retweeted_status"])
    df_retweet_authors = pd.DataFrame(retweets["user"])

    retweeted_idx = df.loc[~df["retweeted_status"].isna()].index

    original_authors = users.iloc[retweeted_idx, :]
    retweet_authors = df_retweet_authors.iloc[retweeted_idx, :]
