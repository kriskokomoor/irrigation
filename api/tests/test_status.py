import requests

BASE_URL = "http://localhost:7999"


def test_status_endpoint_returns_200():
    resp = requests.get(f"{BASE_URL}/status", timeout=3)
    assert resp.status_code == 200


def test_status_structure():
    resp = requests.get(f"{BASE_URL}/status", timeout=3)
    data = resp.json()

    # Expect 4 zones
    assert "zone1" in data
    assert "zone2" in data
    assert "zone3" in data
    assert "zone4" in data

    # Expect boolean values
    assert isinstance(data["zone1"], bool)
    assert isinstance(data["zone2"], bool)
    assert isinstance(data["zone3"], bool)
    assert isinstance(data["zone4"], bool)
