import time
import pytest
from jsonschema import validate, ValidationError

# JSON schema for the minimal expected response structure (current_weather present)
WEATHER_SCHEMA = {
    "type": "object",
    "properties": {
        "latitude": {"type": "number"},
        "longitude": {"type": "number"},
        "generationtime_ms": {"type": "number"},
        "utc_offset_seconds": {"type": "number"},
        "timezone": {"type": "string"},
        "current_weather": {
            "type": "object",
            "properties": {
                "temperature": {"type": "number"},
                "windspeed": {"type": "number"},
                "winddirection": {"type": "number"},
                "weathercode": {"type": "number"},
                "time": {"type": "string"}
            },
            "required": ["temperature", "windspeed", "winddirection", "time"]
        }
    },
    "required": ["latitude", "longitude", "current_weather"]
}

@pytest.mark.parametrize("lat,lon,desc", [
    (28.7041, 77.1025, "New Delhi, India"),
    (51.5074, -0.1278, "London, UK"),
    (40.7128, -74.0060, "New York, USA"),
])
def test_current_weather_status_and_schema(session, base_url, lat, lon, desc):
    """Positive test: status code + basic schema validation for multiple cities."""
    params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
    res = session.get(base_url, params=params, timeout=10)
    assert res.status_code == 200, f"Status {res.status_code} for {desc}"

    data = res.json()
    # Validate presence of current_weather and apply schema
    try:
        validate(instance=data, schema=WEATHER_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"Schema validation failed for {desc}: {e}")

    # Extra sanity checks on value ranges (broad)
    curr = data.get("current_weather", {})
    assert -100 <= curr["temperature"] <= 70, f"Temperature out of bounds for {desc}"
    assert 0 <= curr["windspeed"] <= 200, f"Windspeed out of bounds for {desc}"

def test_response_time_threshold(session, base_url):
    """Fail if endpoint takes too long — basic performance check."""
    params = {"latitude": 28.7041, "longitude": 77.1025, "current_weather": "true"}
    start = time.time()
    res = session.get(base_url, params=params, timeout=10)
    elapsed_ms = (time.time() - start) * 1000
    assert res.status_code == 200
    # set a soft threshold: 1200 ms
    assert elapsed_ms < 1200, f"API too slow: {elapsed_ms:.0f} ms"
