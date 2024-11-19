"""Pytest global configurations."""

import json

import pytest

SAMPLE_METADATA = dict(
    short_title="Sample Metadata",
    long_title="Dummy LONG LONG LONG LONG Title",
    organization="Dummy Organization",
    submit_date="2000-00-00",
    submit_date_qc="2000-00-00",
    submit_date_posted="2000-00-00",
    results_date="2000-00-00",
    results_date_qc="2000-00-00",
    results_date_posted="2000-00-00",
    last_update_date="2000-00-00",
    last_update_date_posted="2000-00-00",
    verify_date="2000-00-00",
    sponsor="Dummy Sponsor",
    collaborators=json.dumps(["Collaborator 1", "Collaborator 2"]),
    summary="Dummy summary.",
    details="Dummy details.",
    conditions=json.dumps(["Condition 1", "Condition 2"]),
    study_phases="NA",
    study_type="INTERVENTIONAL",
    enrollment_count=100,
    allocation="RANDOMIZED",
    intervention_model="PARALLEL",
    observational_model="",
    primary_purpose="TREATMENT",
    who_masked="",
    interventions=json.dumps(
        [
            {
                "type": "BEHAVIORAL",
                "name": "Intervention 1",
                "description": "Description 1.",
            }
        ]
    ),
    primary_measure_outcomes=json.dumps(
        [
            {
                "measure": "Measure 1",
                "description": "Description 1",
                "time_frame": "6 months",
            },
            {
                "measure": "Measure 2",
                "description": "Description 2",
                "time_frame": "4 months",
            },
        ],
    ),
    secondary_measure_outcomes=json.dumps([]),
    other_measure_outcomes=json.dumps([]),
    min_age=18,
    max_age=30,
    eligible_sex="ALL",
    accepts_healthy=False,
    inclusion_criteria="Inclusion Criteria 1. Inclusion Criteria 2.",
    exclusion_criteria="Exclusion Criteria 1. Exclusion Criteria 2.",
    officials=json.dumps(["Official 1", "Official 2"]),
    locations=json.dumps(["Location 1", "Location 2"]),
    references=json.dumps([{"pmid": "dummy-id1", "citation": "Citation 1"}]),
    documents=json.dumps([{"url": "https://dummy-url1", "size": 1000}]),
)


class MockChromadbCollection:
    RECORDS = {"id1", "id2", "id3", "id4"}

    def get(
        self,
        ids=None,
        where=None,
        limit=None,
        offset=None,
        where_document=None,
        include=["metadatas", "documents"],
    ):
        result = dict(
            ids=[],
            documents=[] if "documents" in include else None,
            metadatas=[] if "metadatas" in include else None,
            include=include,
        )

        for key in ids:
            if key not in self.RECORDS:
                raise ValueError(f"Record {key} not found.")
            result["ids"].append(key)
            if "documents" in include:
                result["documents"].append(f"doc-{key}")
            if "metadatas" in include:
                metadata = SAMPLE_METADATA.copy()
                metadata["short_title"] = f"Sample Metadata {key}"
                result["metadatas"].append(metadata)

        return result


@pytest.fixture
def sample_metadata():
    return SAMPLE_METADATA


@pytest.fixture
def chromadb_collection():
    return MockChromadbCollection()
