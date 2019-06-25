import networkx as nx
import pandas as pd
from  src.utils.database_connection_handler import *
import ast


def insert_values(conn, tweets, users):
    """
    """

    for tweets, users in zip(tweets, users):
        print(tweets,  users)
        tweet_id = create_tweets(conn, tweets)
        create_users(conn, users, tweet_id)

    print("Finished inserting values")

def create_tweets(conn, tweet):
    """
    """
    cur = conn.cursor()
    sql = ''' INSERT INTO tweets(id, created_at, text)
                     VALUES(?,?,?) '''
    cur.execute(sql, tweet)
    conn.commit()
    return cur.lastrowid

def create_users(conn, user, tweet_id):
    """

    """
    import numpy as np
    cur = conn.cursor()
    sql = ''' INSERT INTO users(screen_name, description, tweets_id)
                     VALUES(?,?,?) '''
    user_with_fk = np.insert(user, 2, tweet_id)
    cur.execute(sql, user_with_fk)
    conn.commit()



def select_all_users(conn):
    """
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def create_df(df):
    entity = df.fillna("{}")

    entity = entity.apply(ast.literal_eval)

    tmp = entity.values.tolist()

    entity = pd.DataFrame(tmp)

    return entity


if __name__ == '__main__':

    df = pd.read_csv("/home/tcake/coding_projects/python/opt_out/fixed_metoo_tweets.csv")

    some_tweets = df[["id", "created_at", "text"]]
    t=  [tuple(row) for row in some_tweets.values]

    users = create_df(df['user'])
    some_users = users[['screen_name', 'description']]
    u =  [tuple(row) for row in some_users.values]


    database = "metoo.db"

    sql_create_tweets_table = """ CREATE TABLE IF NOT EXISTS tweets (
                                        id integer PRIMARY KEY,
                                        created_at text NOT NULL,
                                        text text NOT NULL
                                    ); """

    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    screen_name text NOT NULL,
                                    description text,
                                    tweets_id integer NOT NULL,
                                    FOREIGN KEY (tweets_id) REFERENCES tweets (id)
                                );"""

    conn = create_connection(database)
    if conn is not None:

        create_table(conn, sql_create_tweets_table)

        create_table(conn, sql_create_users_table)
    else:
        print("Error! cannot create the database connection.")

    insert_values(conn, t, u)
    select_all_users(conn)
    conn.close()
