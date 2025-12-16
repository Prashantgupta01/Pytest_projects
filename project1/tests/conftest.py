import pytest
import requests

@pytest.fixture
def base_url():
    return "https://api.attackontitanapi.com"