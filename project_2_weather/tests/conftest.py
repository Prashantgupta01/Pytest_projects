import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    # Open-Meteo base endpoint
    return "https://api.open-meteo.com/v1/forecast"

@pytest.fixture
def session():
    s = requests.Session()
    yield s
    s.close()