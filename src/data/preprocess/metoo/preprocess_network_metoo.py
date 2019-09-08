import ast

import pandas as pd


def create_df(dataframe):
    entity = dataframe.fillna("{}")

    entity = entity.apply(ast.literal_eval)

    tmp = entity.values.tolist()

    entity = pd.DataFrame(tmp)

    return entity


if __name__ == "__main__":
    DATAFRAME = pd.read_csv("../../../../data/interim/sample_metoo_tweets.csv")
    USERS = create_df(DATAFRAME["user"])
    ENTITIES = create_df(DATAFRAME["ENTITIES"])
    RETWEETS = create_df(DATAFRAME["retweeted_status"])
    DF_RETWEET_AUTHORS = pd.DataFrame(RETWEETS["user"])

    RETWEETED_IDX = DATAFRAME.loc[~DATAFRAME["retweeted_status"].isna()].index

    ORIGINAL_AUTHORS = USERS.iloc[RETWEETED_IDX, :]
    RETWEET_AUTHORS = DF_RETWEET_AUTHORS.iloc[RETWEETED_IDX, :]
