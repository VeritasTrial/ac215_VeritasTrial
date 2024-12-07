"""Test the utils module."""

import json

import numpy as np
import pytest

from utils import format_exc_details, get_metadata_from_id


def _snake_to_camel(snake_str):
    """Helper function to convert snake case to camel case."""
    parts = snake_str.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


def test_format_exc_details():
    """Test formatting exception details."""
    try:
        np.sum("")  # Error
    except Exception as e:
        # NOTE: There is no need to mock the path because this test file has the
        # same parent directory as the tested module
        details = format_exc_details(e)

        assert "numpy" not in details  # Internals are not mentioned
        assert e.__class__.__name__ in details
        assert str(e) in details
        assert "in test_format_exc_details" in details
        assert 'np.sum("")' in details


@pytest.mark.parametrize("item_id", ["id0", "id1", "id2"])
def test_get_metadata_from_id(item_id, chromadb_client, sample_metadata):
    collection = chromadb_client.get_collection("test")
    metadata = get_metadata_from_id(collection, item_id)
    assert metadata["shortTitle"] == f"Sample Metadata {item_id}"

    for key, value in sample_metadata.items():
        if key == "short_title":
            pass  # Already checked
        elif key in (
            "collaborators",
            "conditions",
            "interventions",
            "officials",
            "locations",
            "references",
            "documents",
        ):
            # Flat lists or list of dictionaries that do not need case conversion
            assert metadata[_snake_to_camel(key)] == json.loads(value)
        elif key.endswith("_measure_outcomes"):
            # List of dictionaries that need case conversion
            for item, item_exp in zip(
                metadata[_snake_to_camel(key)], json.loads(value), strict=True
            ):
                assert item["measure"] == item_exp["measure"]
                assert item["description"] == item_exp["description"]
                assert item["timeFrame"] == item_exp["time_frame"]
        else:
            assert metadata[_snake_to_camel(key)] == value
