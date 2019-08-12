import networkx as nx
import pandas as pd
import ast
import matplotlib.pyplot as plt

def create_df(df):
    entity = df.fillna("{}")

    entity = entity.apply(ast.literal_eval)

    tmp = entity.values.tolist()

    entity = pd.DataFrame(tmp)

    return entity


if __name__ == '__main__':

    df = pd.read_csv("../../../../data/interim/sample_metoo_tweets.csv")
    users = create_df(df['user'])
    entities =  create_df(df['entities'])
    retweets = create_df(df['retweeted_status'])
    df_retweet_authors = pd.DataFrame(retweets['user'])

    retweeted_idx = df.loc[~df["retweeted_status"].isna()].index

    original_authors = users.iloc[retweeted_idx, :]
    retweet_authors = df_retweet_authors.iloc[retweeted_idx, :]

    graph = nx.Graph()

    for o_name, r_name  in zip(original_authors['name'],retweet_authors['user']):
         graph.add_edge(o_name, r_name['name'])

    options = {
        'node_color': 'black',
        'node_size': 50,
        'line_color': 'grey',
        'linewidths': 0,
        'width': 0.1,
    }
    nx.draw(graph, **options)
    plt.savefig("yes.png")

    plt.show()
