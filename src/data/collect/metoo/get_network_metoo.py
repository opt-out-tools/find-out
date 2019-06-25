import json
import click
import mock
import pandas as pd
import pytest
import tweepy


@click.command()
@click.option("--path_to_creds", "-creds", required=True, help="path to twitter credentials")
@click.option("--path_to_ids", "-ids", required=True, help="path to tweet ids")
@click.option("--path_to_output", "-o", required=True, help="path to where the tweets should be written to")
def main(path_to_creds, path_to_ids, path_to_output):
    """ Runs the functions that enable tweets to be gathered by id and saved to csv. """
    credentials = read_json(path_to_creds)

    api = create_twitter_API_connection(credentials)

    gather_tweets(api, path_to_ids, path_to_output, 256455)


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


def gather_tweets(api, path_to_ids, path_to_output, starting_id_idx=0):
    """
    """
    ids = pd.read_csv(path_to_ids)

    tweets = []
    counter = 0
    for n, row in ids.iloc[starting_id_idx:, : ].iterrows():
        if n < len(ids):
            try:
                id_of_tweet = row['id']
                tweets.append(api.get_status(id_of_tweet)._json)
                print(f"Tweet id # {n}", id_of_tweet)

            except:
                print(str(id_of_tweet) + ' tweet does not exist anymore')

            if n % 1000 == 0:
                if n == 0:
                    write_to_disk(tweets, True, path_to_output)
                else:
                    write_to_disk(tweets, False, path_to_output)

                counter += len(tweets)
                print(f"{counter} tweets have been saved to file")
                tweets = []


def write_to_disk(tweets, save_headers, path_to_output):
    """ Writes the dataframe to a csv file, appending further tweets with the tweet object keys as columns,"""
    tweet_object_keys = ['contributors', 'coordinates', 'entities',
                         'extended_entities', 'favorite_count', 'favorited', 'geo',
                         'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id',
                         'in_reply_to_status_id_str', 'in_reply_to_user_id',
                         'in_reply_to_user_id_str', 'is_quote_status', 'lang', 'place',
                         'possibly_sensitive', 'possibly_sensitive_appealable', 'quoted_status',
                         'quoted_status_id', 'quoted_status_id_str', 'retweet_count',
                         'retweeted', 'retweeted_status', 'source', 'truncated', 'user']

    df = pd.DataFrame(tweets, columns=tweet_object_keys)
    df.to_csv(path_to_output, mode="a", index=False, header=save_headers)
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
        create_twitter_API_connection({"CONSUMER_KEY": "key", "CONSUMER_SECRET": "secret", "ACCESS_TOKEN": "token",
                                       "ACCESS_SECRET": "access_secret"})
    assert str(e.value) == "Failed to send request, invalid credentials."


# TODO finish mocking/testing gather_tweets
# def test_api_call():
#     with mock.patch('tweepy.api') as mocked_tweepy:
#         with mock.patch('pandas.read_csv', mock.mock_open(read_data="{'id': [12345]}")):
#             mock.mock_open.iterrows.return_value = (0, 12345)
#             gather_tweets(mocked_tweepy, mock.mock_open,"")
#         mocked_tweepy.get_status.assert_called_once()


if __name__ == "__main__":
    main()
