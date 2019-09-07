import json

import click
import mock
import pandas as pd
import tweepy


@click.command()
@click.option("--path_to_creds", "-creds", required=True,
              help="path to twitter credentials")
@click.option("--path_to_ids", "-ids", required=True, help="path to tweet ids")
@click.option("--path_to_output", "-o", required=True,
              help="path to where the tweets should be written to", )
def main(path_to_creds, path_to_ids, path_to_output):
    """ Runs the functions that enable tweets to be gathered by id and saved
    to csv. """

    credentials = read_json(path_to_creds)

    api = create_twitter_api_connection(credentials)

    gather_tweets(api, path_to_ids, path_to_output, 256455)


def read_json(path):
    """ Reads in the twitter credentials in json format and converts them to
    a dictionary. """
    try:
        with open(path, "r") as file:
            creds = json.load(file)
        file.close()

    except FileNotFoundError:
        raise FileNotFoundError("The path to your twitter credentials is not correct.")

    return creds


def create_twitter_api_connection(creds):
    """ Returns the connection to the twitter API. """

    auth = tweepy.OAuthHandler(creds["CONSUMER_KEY"], creds["CONSUMER_SECRET"])
    auth.set_access_token(creds["ACCESS_TOKEN"], creds["ACCESS_SECRET"])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.me()
    except Exception:
        raise Exception("Failed to send request, invalid credentials.")

    return api


def gather_tweets(api, path_to_ids, path_to_output, starting_id_idx=0):
    """ Writes tweets returned from the /show/status API to csv file every
    1000 API calls. If the tweet is not there
        a message is displayed in the stdout.
    """
    ids = pd.read_csv(path_to_ids)

    tweets = []
    counter = 0
    for n, row in ids.iloc[starting_id_idx:, :].iterrows():
        if n < len(ids):
            try:
                id_of_tweet = row["id"]
                tweets.append(api.get_status(id_of_tweet)._json)
                print(f"Tweet id # {n}", id_of_tweet)

            except:
                print(str(id_of_tweet) + " tweet does not exist anymore")

            if n % 1000 == 0:
                if n == 0:
                    write_to_disk(tweets, True, path_to_output)
                else:
                    write_to_disk(tweets, False, path_to_output)

                counter += len(tweets)
                print(f"{counter} tweets have been saved to file")
                tweets = []


def write_to_disk(tweets, save_headers, path_to_output):
    """ Writes the dataframe to a csv file, appending further tweets with
    the tweet object keys as columns,"""
    tweet_object_keys = [
        "contributors",
        "coordinates",
        "entities",
        "extended_entities",
        "favorite_count",
        "favorited",
        "geo",
        "id_str",
        "in_reply_to_screen_name",
        "in_reply_to_status_id",
        "in_reply_to_status_id_str",
        "in_reply_to_user_id",
        "in_reply_to_user_id_str",
        "is_quote_status",
        "lang",
        "place",
        "possibly_sensitive",
        "possibly_sensitive_appealable",
        "quoted_status",
        "quoted_status_id",
        "quoted_status_id_str",
        "retweet_count",
        "retweeted",
        "retweeted_status",
        "source",
        "truncated",
        "user",
    ]

    dataframe = pd.DataFrame(tweets, columns=tweet_object_keys)
    dataframe.to_csv(path_to_output, mode="a", index=False, header=save_headers)
    print("Saved to file")


def test_read_json_returns_dict():
    with mock.patch("builtins.open", mock.mock_open(read_data="{}")):
        credentials = read_json(mock.mock_open)
    assert isinstance(credentials, dict)
