import json

import requests
import pytest
import jsonschema

from project1.tests.conftest import base_url


def test_randon_quotes_status(base_url):
    res = requests.get(f"{base_url}/episodes")
    assert res.status_code == 200

def test_random_quotes_fields(base_url):
    res = requests.get(f"{base_url}/episodes")
    data = res.json()
    assert "info" in data
    assert "results" in data
    for items in data["results"]:
        print(type(items["id"]))
        assert type(items["id"]) == int
        assert type(items["name"]) == str
        assert type(items["img"]) == str
        assert type(items["episode"]) == str
        assert type(items[ "characters"]) != []
