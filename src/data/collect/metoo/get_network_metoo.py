import tweepy
import json
import pandas as pd
import click
import pytest

@click.command()
@click.option("--path_to_creds","-creds", required=True, help="path to twitter credentials")
@click.option("--path_to_ids", "-ids",required=True, help="path to tweet ids")
@click.option("--path_to_output", "-o",required=True, help="path to where the tweets should be written to")

def main(path_to_creds, path_to_ids):
    api = create_twitter_connection(path_to_creds)


def create_twitter_connection(path):
    """ Returns the connection to the twitter API. """
    try:
        with open(path, "r") as file:
            creds = json.load(file)
        file.close()

        auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
        auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    except FileNotFoundError:
        raise FileNotFoundError("The path to your twitter credentials is not correct.")

    return api

def returns_tweet(path_to_ids, path_to_output, api):
    ids = pd.read_csv(path_to_ids)

    tweet_list = []
    for i, row in ids.iterrows():
        if i < 2:
            try:
                id_of_tweet = row['id']
                tweet_list.append(api.get_status(id_of_tweet)._json)
                print(api.get_status(id_of_tweet)._json)
                print(id_of_tweet)
            except:
                print(str(id_of_tweet) + ' tweet does not exist anymore')

        if i % 100 == 0:
            df = pd.DataFrame(tweet_list)
            df.to_csv(path_to_output, mode="a", index = False)
            tweet_list = []
            print("Saved to file")

@pytest.fixture
def api(path_to_creds):
    return create_twitter_connection(path_to_creds)


def test_throws_exception_if_file_not_found():
    with pytest.raises(FileNotFoundError) as fnf:
        create_twitter_connection("")
    assert str(fnf.value) == "The path to your twitter credentials is not correct."

# TODO def test_does_something_if_incorrect_credentials()

def test_creates_api(api):
    assert api is not None

def test_retrieves_tweet(api):
    response = api.get_status("926911797885657088")._json
    assert response is not None



