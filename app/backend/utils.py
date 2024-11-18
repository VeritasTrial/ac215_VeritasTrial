import json
import traceback
from pathlib import Path
from typing import Any

import chromadb
import chromadb.api

from localtyping import TrialMetadataType


def format_exc_details(exc: Exception) -> str:
    """Format details of an exception."""
    if exc.__traceback__ is None:
        return f"{exc.__class__.__name__}: {exc}"

    base_dir = str(Path(__file__).parent)
    tb = traceback.extract_tb(exc.__traceback__)
    tb_details = "".join(
        traceback.format_list(
            frame for frame in tb if frame.filename.startswith(base_dir)
        )
    )
    return f"{tb_details}\n{exc.__class__.__name__}: {exc}"


def _clean_metadata(metadata: Any) -> TrialMetadataType:
    """Clean metadata stored in ChromaDB into full JSON."""
    return dict(
        shortTitle=metadata["short_title"],
        longTitle=metadata["long_title"],
        organization=metadata["organization"],
        submitDate=metadata["submit_date"],
        submitDateQc=metadata["submit_date_qc"],
        submitDatePosted=metadata["submit_date_posted"],
        resultsDate=metadata["results_date"],
        resultsDateQc=metadata["results_date_qc"],
        resultsDatePosted=metadata["results_date_posted"],
        lastUpdateDate=metadata["last_update_date"],
        lastUpdateDatePosted=metadata["last_update_date_posted"],
        verifyDate=metadata["verify_date"],
        sponsor=metadata["sponsor"],
        collaborators=json.loads(metadata["collaborators"]),
        summary=metadata["summary"],
        details=metadata["details"],
        conditions=json.loads(metadata["conditions"]),
        studyPhases=metadata["study_phases"],
        studyType=metadata["study_type"],
        enrollmentCount=metadata["enrollment_count"],
        allocation=metadata["allocation"],
        interventionModel=metadata["intervention_model"],
        observationalModel=metadata["observational_model"],
        primaryPurpose=metadata["primary_purpose"],
        whoMasked=metadata["who_masked"],
        interventions=[
            dict(
                type=item["type"],
                name=item["name"],
                description=item["description"],
            )
            for item in json.loads(metadata["interventions"])
        ],
        primaryMeasureOutcomes=[
            dict(
                measure=item["measure"],
                description=item["description"],
                timeFrame=item["time_frame"],
            )
            for item in json.loads(metadata["primary_measure_outcomes"])
        ],
        secondaryMeasureOutcomes=[
            dict(
                measure=item["measure"],
                description=item["description"],
                timeFrame=item["time_frame"],
            )
            for item in json.loads(metadata["secondary_measure_outcomes"])
        ],
        otherMeasureOutcomes=[
            dict(
                measure=item["measure"],
                description=item["description"],
                timeFrame=item["time_frame"],
            )
            for item in json.loads(metadata["other_measure_outcomes"])
        ],
        minAge=metadata["min_age"],
        maxAge=metadata["max_age"],
        eligibleSex=metadata["eligible_sex"],
        acceptsHealthy=metadata["accepts_healthy"],
        inclusionCriteria=metadata["inclusion_criteria"],
        exclusionCriteria=metadata["exclusion_criteria"],
        officials=json.loads(metadata["officials"]),
        locations=json.loads(metadata["locations"]),
        references=[
            dict(
                pmid=item["pmid"],
                citation=item["citation"],
            )
            for item in json.loads(metadata["references"])
        ],
        documents=[
            dict(
                url=item["url"],
                size=item["size"],
            )
            for item in json.loads(metadata["documents"])
        ],
    )


def _get_metadata_from_id(
    collection: chromadb.Collection, item_id: str
) -> TrialMetadataType | None:
    """Get metadata from a document ID."""
    results = collection.get(
        ids=[item_id], include=[chromadb.api.types.IncludeEnum("metadatas")]
    )
    metadatas = results["metadatas"]
    if metadatas is None:
        return None
    return _clean_metadata(metadatas[0])
