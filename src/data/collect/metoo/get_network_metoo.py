import tweepy
import json
import pandas as pd
import click
import pytest
import mock

@click.command()
@click.option("--path_to_creds","-creds", required=True, help="path to twitter credentials")
@click.option("--path_to_ids", "-ids",required=True, help="path to tweet ids")
@click.option("--path_to_output", "-o",required=True, help="path to where the tweets should be written to")
def main(path_to_creds, path_to_ids, path_to_output):

    credentials = read_json(path_to_creds)

    api = create_twitter_API_connection(credentials)

    gather_tweets(api, path_to_ids, path_to_output)

def read_json(path):
    """ Reads in the twitter credentials in json format and converts them to a dictionary. """
    try:
        with open(path, "r") as file:
            creds = json.load(file)
        file.close()

    except FileNotFoundError:
        raise FileNotFoundError("The path to your twitter credentials is not correct.")

    return creds

def create_twitter_API_connection(creds):
    """ Returns the connection to the twitter API. """

    auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.me()
    except Exception as e:
        raise Exception('Failed to send request, invalid credentials.')

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



def test_read_json_returns_dict():
    with mock.patch('builtins.open', mock.mock_open(read_data='{}')):
        credentials = read_json(mock.mock_open)
    assert isinstance(credentials, dict)

def test_throws_exception_if_file_not_found():
    with pytest.raises(FileNotFoundError) as fnf:
        read_json("")
    assert str(fnf.value) == "The path to your twitter credentials is not correct."

def test_raises_exception_if_incorrect_credentials():
    with pytest.raises(Exception) as e:
        create_twitter_API_connection({"CONSUMER_KEY" : "key", "CONSUMER_SECRET": "secret", "ACCESS_TOKEN": "token", "ACCESS_SECRET": "access_secret" })
    assert str(e.value) == "Failed to send request, invalid credentials."




if __name__ == "__main__":
    main()
