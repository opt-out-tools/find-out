import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--path_to_creds", action="store", help="path to twitter credentials"
    )
    parser.addoption(
        "--path_to_ids", action="store", help="path to tweet ids"
    )

@pytest.fixture
def path_to_creds(request):
    return request.config.getoption("--path_to_creds")

@pytest.fixture
def path_to_ids(request):
    return request.config.getoption("--path_to_ids")
