import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi.testclient import TestClient
from main import app
from config import MAX_BITS

client = TestClient(app)


def test_valid_request_returns_bits():
    response = client.post("/quantum/bits", json={"groups": {"a": 3, "b": 5}})
    assert response.status_code == 200
    data = response.json()
    assert set(data["bits"].keys()) == {"a", "b"}
    assert len(data["bits"]["a"]) == 3
    assert len(data["bits"]["b"]) == 5
    assert "backend" in data


def test_empty_attribute_name_rejected():
    response = client.post("/quantum/bits", json={"groups": {"": 3}})
    assert response.status_code == 422


def test_over_cap_rejected():
    response = client.post("/quantum/bits", json={"groups": {"a": MAX_BITS + 1}})
    assert response.status_code == 422


def test_negative_count_rejected():
    response = client.post("/quantum/bits", json={"groups": {"a": -3}})
    assert response.status_code == 422
