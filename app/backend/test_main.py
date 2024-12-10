"""Test the main module."""

import json
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_heartbeat():
    """Test the /heartbeat endpoint."""
    response = client.get("/heartbeat")
    assert response.status_code == 200
    response_json = response.json()
    assert "timestamp" in response_json


@pytest.mark.parametrize("top_k", [1, 3, 5])
def test_retrieve(top_k):
    """Test the /retrieve endpoint."""
    filters_serialized = quote(json.dumps({}))
    response = client.get(
        f"/retrieve?query=Dummy Query&{top_k=}&filters_serialized={filters_serialized}"
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "ids" in response_json
    assert "documents" in response_json
    assert len(response_json["ids"]) == top_k
    assert len(response_json["documents"]) == top_k


@pytest.mark.parametrize("top_k", [0, 31])
def test_retrieve_invalid_top_k(top_k):
    """Test the /retrieve endpoint with invalid top_k."""
    filters_serialized = quote(json.dumps({}))
    response = client.get(
        f"/retrieve?query=Dummy Query&{top_k=}&filters_serialized={filters_serialized}"
    )
    assert response.status_code == 404
    assert "Required 0 < top_k <= 30" in response.text


@pytest.mark.parametrize("item_id", ["id0", "id1", "id2"])
def test_meta(item_id):
    """Test the /meta/{item_id} endpoint."""
    response = client.get(f"/meta/{item_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert "metadata" in response_json
    assert response_json["metadata"]["shortTitle"] == f"Sample Metadata {item_id}"


# TODO: Add tests for the /chat/{model}/{item_id} endpoint
