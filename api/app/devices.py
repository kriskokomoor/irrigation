import requests
from .config import ESP32_BASE_URL

def set_zone(zone_id: int, state: str):
    url = f"{ESP32_BASE_URL}/zone/{zone_id}/{state}"
    resp = requests.post(url, timeout=5)
    resp.raise_for_status()
    return resp.text

def get_status():
    url = f"{ESP32_BASE_URL}/status"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json()
