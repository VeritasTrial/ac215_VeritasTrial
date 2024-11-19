"""Test the main module."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_heartbeat():
    """Test the /heartbeat endpoint."""
    response = client.get("/heartbeat")
    assert response.status_code == 200
    assert "timestamp" in response.json()
