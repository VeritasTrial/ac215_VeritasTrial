"""Test the utils module."""

import json

import numpy as np
import pytest

from utils import construct_filters, format_exc_details, get_metadata_from_id


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
    """Test getting metadata from an item ID."""
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


@pytest.mark.parametrize(
    "filters, expected_where, expected_needs_post_filter",
    [
        # Single filter
        ({"studyType": "interventional"}, {"study_type": "INTERVENTIONAL"}, False),
        ({"acceptsHealthy": False}, {"accepts_healthy": False}, False),
        ({"acceptsHealthy": True}, None, False),
        ({"eligibleSex": "female"}, {"eligible_sex": "FEMALE"}, False),
        (
            {"ageRange": (18, 30)},
            {"$and": [{"min_age": {"$lte": 30}}, {"max_age": {"$gte": 18}}]},
            False,
        ),
        # Multiple filters
        (
            {"studyType": "interventional", "acceptsHealthy": False},
            {"$and": [{"study_type": "INTERVENTIONAL"}, {"accepts_healthy": False}]},
            False,
        ),
        (
            {"eligibleSex": "female", "ageRange": (18, 30)},
            {
                "$and": [
                    {"eligible_sex": "FEMALE"},
                    {"min_age": {"$lte": 30}},
                    {"max_age": {"$gte": 18}},
                ]
            },
            False,
        ),
        # Expected post-processing
        ({"studyPhases": ["PHASE1"]}, None, True),
        ({"lastUpdateDatePosted": (0, 0)}, None, True),
        ({"resultsDatePosted": (0, 0)}, None, True),
    ],
)
def test_construct_filters(filters, expected_where, expected_needs_post_filter):
    """Test constructing filters."""
    assert construct_filters(filters) == (expected_needs_post_filter, expected_where)


# TODO: Add tests for the post_filter function
