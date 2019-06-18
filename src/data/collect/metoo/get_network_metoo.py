import tweepy
import json
import pandas as pd
import click
import pytest

@click.command()
@click.option("--path_to_creds","-creds", required=True, help="path to twitter credentials")
@click.option("--path_to_ids", "-ids",required=True, help="path to tweet ids")
@click.option("--path_to_output", "-o",required=True, help="path to where the tweets should be written to")
def main(path_to_creds, path_to_ids, path_to_output):
    api = create_twitter_connection(path_to_creds)
    gather_tweets(api, path_to_ids, path_to_output)

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

def gather_tweets(api, path_to_ids, path_to_output):
    """

    """
    ids = pd.read_csv(path_to_ids)

    tweets = []
    counter = 0
    for n, row in ids.iterrows():
        if n < len(ids):
            try:
                id_of_tweet = row['id']
                tweets.append(api.get_status(id_of_tweet)._json)
                print(f"Tweet id # {n}", id_of_tweet)

            except:
                print(str(id_of_tweet) + ' tweet does not exist anymore')

            if n % 1000 == 0:
                write_to_disk(tweets, n, path_to_output)
                counter +=len(tweets)
                print(f"{counter} tweets have been saved to file")
                tweets = []


def write_to_disk(tweets, counter, path_to_output):
    """
    """
    df = pd.DataFrame(tweets)
    df.to_csv(path_to_output, mode="a", index=False, header=True)
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



main()
