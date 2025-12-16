import pytest

def test_missing_parameters(session, base_url):
    """Negative test: missing lat/lon returns 400 or helpful error/documented behavior."""
    # Provide no params
    res = session.get(base_url, timeout=10)
    # Open-Meteo returns 400 if required params missing, but behavior may vary.
    # Accept either 400 or 422 or even 200 with an empty response. Assert it's not successful with current_weather.
    assert res.status_code in (200, 400, 422), "Unexpected status code for missing params"
    # If 200, ensure current_weather is not present
    try:
        data = res.json()
    except ValueError:
        # Not JSON — acceptable for negative case
        return

    assert "current_weather" not in data, "current_weather should not be present when params missing"

@pytest.mark.parametrize("lat,lon", [
    ("abc", 77.1025),
    (28.7041, "xyz"),
    ("", ""),
])
def test_invalid_parameter_values(session, base_url, lat, lon):
    """Invalid coordinate types should be handled gracefully."""
    params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
    res = session.get(base_url, params=params, timeout=10)
    # Most likely API returns 400 or 422; accept 200 only if current_weather absent
    assert res.status_code in (200, 400, 422)
    if res.status_code == 200:
        try:
            data = res.json()
        except ValueError:
            return
        assert "current_weather" not in data
