"""Utilities for the backend APIs."""

import json
import traceback
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Any, Literal

import chromadb
import chromadb.api

from localtyping import APIRetrieveResponseType, TrialFilters, TrialMetadataType


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


def get_metadata_from_id(
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


def construct_filters(filters: TrialFilters) -> tuple[bool, chromadb.Where | None]:
    """Construct filters for querying trials."""
    processed_filters: list[chromadb.Where] = []

    if (study_type := filters.get("studyType")) is not None:
        processed_filters.append({"study_type": study_type.upper()})

    if (
        accepts_healthy := filters.get("acceptsHealthy")
    ) is not None and not accepts_healthy:
        # NOTE: The accepts_healthy filter being True means that the study accepts
        # healthy participants; yet unhealthy participants are always accepted, so it is
        # equivalent to not having this filter at all
        processed_filters.append({"accepts_healthy": False})

    if (eligible_sex := filters.get("eligibleSex")) is not None:
        processed_filters.append({"eligible_sex": eligible_sex.upper()})

    if (age_range := filters.get("ageRange")) is not None:
        # NOTE: We want the age range to intersect with the desired range, so it
        # suffices to have actual minimum <= desired maximum and actual maximum >=
        # desired minimum
        min_age, max_age = age_range
        processed_filters.append({"min_age": {"$lte": max_age}})  # type: ignore
        processed_filters.append({"max_age": {"$gte": min_age}})  # type: ignore

    # Construct the where clause
    where: chromadb.Where | None = None
    if len(processed_filters) == 1:
        where = processed_filters[0]
    elif len(processed_filters) > 1:
        where = {"$and": processed_filters}

    # Determine if there are post-processing filters required
    needs_post_filter = any(
        key in filters
        for key in ["studyPhases", "lastUpdateDatePosted", "resultsDatePosted"]
    )

    return needs_post_filter, where


def post_filter(
    results: chromadb.QueryResult, filters: TrialFilters
) -> APIRetrieveResponseType:
    """Post-filtering of query results."""
    filtered_ids, filtered_documents = [], []

    assert (
        results["documents"] is not None and results["metadatas"] is not None
    ), "Missing documents or metadatas required for post-filtering"
    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    def _accept_by_study_phases(metadata: Any, study_phases_filter: list[str]) -> bool:
        # If any of the study phases as in the metadata is in the desired study phases,
        # then we accept this metadata; TODO: ChromaDB should support more flexible
        # string matching on metadata fields, e.g., the $contains operator is currently
        # only supported for document filters but not metadata field filters; by then we
        # will be able to move this post-filtering logic to the database query
        study_phases = metadata["study_phases"].split(", ")
        return any(phase in study_phases_filter for phase in study_phases)

    def _accept_by_date(
        metadata: Any,
        key: Literal["last_update_date_posted", "results_date_posted"],
        date_range_filter: tuple[int, int],
    ) -> bool:
        # If the date field is within the desired range, then we accept this metadata;
        # we note that some data fields in the metadata do not have the day part, but
        # the two types we accept here both do; TODO: we should consider storing the
        # date fields as timestamps in the database so that we can move this
        # post-filtering logic to the database query
        date_from_filter, date_to_filter = date_range_filter
        date = datetime.strptime(metadata[key], "%Y-%m-%d").timestamp() * 1000
        return date_from_filter <= date <= date_to_filter

    # Construc the list of post-filtering functions
    post_filter_funcs = []
    if (study_phase_filter := filters.get("studyPhases")) is not None:
        post_filter_funcs.append(
            partial(_accept_by_study_phases, study_phases_filter=study_phase_filter)
        )
    if (last_update_date_filter := filters.get("lastUpdateDatePosted")) is not None:
        post_filter_funcs.append(
            partial(
                _accept_by_date,
                key="last_update_date_posted",
                date_range_filter=last_update_date_filter,
            )
        )
    if (results_date_filter := filters.get("resultsDatePosted")) is not None:
        post_filter_funcs.append(
            partial(
                _accept_by_date,
                key="results_date_posted",
                date_range_filter=results_date_filter,
            )
        )

    # For each item, append to the filtered list only if all post-filtering functions
    # accept that item
    for _id, document, metadata in zip(ids, documents, metadatas):
        if all(func(metadata) for func in post_filter_funcs):
            filtered_ids.append(_id)
            filtered_documents.append(document)

    return {"ids": filtered_ids, "documents": filtered_documents}
