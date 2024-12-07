"""Pytest global configurations."""

import json

import numpy as np
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


class MockEmbeddingModel:
    """Mock embedding model."""

    def encode(self, query):
        return np.array([0.1, 0.2, 0.3, 0.4, 0.5])


class MockChromadbCollection:
    """Mock ChromaDB collection."""

    RECORDS = set(f"id{i}" for i in range(50))

    def _result(self, ids, include, where):
        result = dict(
            ids=ids,
            documents=[] if "documents" in include else None,
            metadatas=[] if "metadatas" in include else None,
            include=include,
        )

        for key in ids:
            if "documents" in include:
                result["documents"].append(f"doc-{key}")
            if "metadatas" in include:
                metadata = SAMPLE_METADATA.copy()
                metadata["short_title"] = f"Sample Metadata {key}"
                result["metadatas"].append(metadata)
        return result

    def query(self, *, query_embeddings, n_results, include, where=None):
        result = self._result(list(self.RECORDS)[:n_results], include, where)
        for k in result:
            result[k] = [result[k] for _ in range(len(query_embeddings))]
        return result

    def get(self, *, ids, include, where=None):
        return self._result(ids, include, where)


class MockChromadbClient:
    """Mock ChromaDB client."""

    def get_collection(self, name):
        return MockChromadbCollection()


@pytest.fixture
def sample_metadata():
    """Return a fixed sample metadata."""
    return SAMPLE_METADATA


@pytest.fixture
def embedding_model():
    """Return a mock embedding model."""
    return MockEmbeddingModel()


@pytest.fixture
def chromadb_client():
    """Return a mock ChromaDB client."""
    return MockChromadbClient()


@pytest.fixture(autouse=True)
def setup(monkeypatch):
    monkeypatch.setattr("vertexai.init", lambda: None)
    monkeypatch.setattr("main.EMBEDDING_MODEL", MockEmbeddingModel())
    monkeypatch.setattr("main.CHROMADB_CLIENT", MockChromadbClient())
