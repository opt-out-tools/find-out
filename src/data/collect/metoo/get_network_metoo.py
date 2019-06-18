import tweepy
import json
import pandas as pd
import sys
import click

path_to_credentials = sys.argv[1]
path_to_ids = sys.argv[2]
path_to_output = sys.argv[3]

@click.command()
@click.option("--path", default=1, help="path to twitter credentials")
def create_twitter_connection(path):
    """ Returns the connectino to the twiiter API. """
    with open(path, "r") as file:
        creds = json.load(file)
    file.close()

    auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    return api

@click.command()
@click.option("--path", default=1, help="path to tweet ids")
def read_in_ids(path):
    """ Reads in the tweet ids. """
    return pd.read_csv(path_to_ids)


# tweet_list = []
# for i, row in data.iterrows():
#     if i < 2:
#         try:
#             id_of_tweet = row['id']
#             tweet_list.append(api.get_status(id_of_tweet)._json)
#             print(api.get_status(id_of_tweet)._json)
#             print(id_of_tweet)
#         except:
#             print(str(id_of_tweet) + ' tweet does not exist anymore')
#
#         if i % 100 == 0:
#             df = pd.DataFrame(tweet_list)
#             df.to_csv(path_to_output, mode="a", index = False)
#             tweet_list = []
#             print("Saved to file")


def test_returns_json():
    response = api.get_status("926911797885657088")._json
    assert response is not None

create_twitter_connection()
