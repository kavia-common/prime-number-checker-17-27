import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app
# The app is defined in src/api/main.py as `app`
from src.api.main import app

client = TestClient(app)


def test_health_check():
    """Ensure the health check endpoint returns expected payload."""
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Current implementation returns {"message": "Healthy"}
    assert data.get("message") == "Healthy"


@pytest.mark.parametrize("value", [2, 3, 5, 13, 97, 101])
def test_prime_numbers(value):
    """
    Valid primes should return is_prime=true.
    Assumes endpoint: POST /check-prime with JSON body {"number": <int>}.
    """
    resp = client.post("/check-prime", json={"number": value})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data.get("number") == value
    assert data.get("is_prime") is True


@pytest.mark.parametrize("value", [0, 1, 4, 8, 9, 15, 100])
def test_non_prime_numbers(value):
    """
    Valid non-primes should return is_prime=false.
    """
    resp = client.post("/check-prime", json={"number": value})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data.get("number") == value
    assert data.get("is_prime") is False


@pytest.mark.parametrize(
    "payload",
    [
        {"number": "abc"},     # string instead of int
        {"number": 3.14},      # float instead of int
        {"number": None},      # null
        {},                    # missing field
        {"number": []},        # list
        {"number": {}},        # object
    ],
)
def test_invalid_inputs(payload):
    """
    Invalid inputs should be rejected by Pydantic/FastAPI validation with 422.
    """
    resp = client.post("/check-prime", json=payload)
    assert resp.status_code == 422, f"Expected 422, got {resp.status_code}: {resp.text}"
