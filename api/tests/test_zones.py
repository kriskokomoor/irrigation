import requests
import time

BASE_URL = "http://localhost:7999"


def test_turn_zone_on_and_off():
    zone = 1

    # Turn ON
    resp_on = requests.post(
        f"{BASE_URL}/valve/{zone}",
        json={"state": "on"},
        timeout=3
    )
    assert resp_on.status_code == 200

    # Give ESP32 a moment
    time.sleep(0.5)

    status = requests.get(f"{BASE_URL}/status", timeout=3).json()
    assert status[f"zone{zone}"] is True

    # Turn OFF
    resp_off = requests.post(
        f"{BASE_URL}/valve/{zone}",
        json={"state": "off"},
        timeout=3
    )
    assert resp_off.status_code == 200

    time.sleep(0.5)

    status = requests.get(f"{BASE_URL}/status", timeout=3).json()
    assert status[f"zone{zone}"] is False
