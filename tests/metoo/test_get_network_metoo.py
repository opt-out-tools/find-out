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
    with pytest.raises(Exception) as error:
        create_twitter_api_connection(
            {
                "CONSUMER_KEY": "key",
                "CONSUMER_SECRET": "secret",
                "ACCESS_TOKEN": "token",
                "ACCESS_SECRET": "access_secret",
            }
        )
    assert str(error.value) == "Failed to send request, invalid credentials."
