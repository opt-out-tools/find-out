import pytest

from src.data.collect.metoo.get_network_metoo import (
    create_twitter_api_connection,
    read_json,
)


def test_throws_exception_if_file_not_found():
    with pytest.raises(FileNotFoundError) as fnf:
        read_json("")
    assert str(fnf.value) == "The path to your twitter credentials is not correct."


def test_raises_exception_if_incorrect_credentials():
    with pytest.raises(Exception) as e:
        create_twitter_api_connection(
            {
                "CONSUMER_KEY": "key",
                "CONSUMER_SECRET": "secret",
                "ACCESS_TOKEN": "token",
                "ACCESS_SECRET": "access_secret",
            }
        )
    assert str(e.value) == "Failed to send request, invalid credentials."


# TODO finish mocking/testing gather_tweets
# def test_api_call():
#     with mock.patch('tweepy.api') as mocked_tweepy:
#         with mock.patch('pandas.read_csv', mock.mock_open(read_data="{
#         'id': [12345]}")):
#             mock.mock_open.iterrows.return_value = (0, 12345)
#             gather_tweets(mocked_tweepy, mock.mock_open,"")
#         mocked_tweepy.get_status.assert_called_once()
