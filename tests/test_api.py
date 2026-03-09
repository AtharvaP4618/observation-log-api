import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from run import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"

def test_get_observations(client):
    response = client.get("/observations")
    assert response.status_code == 200