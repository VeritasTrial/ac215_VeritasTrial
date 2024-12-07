"""Type definitions for the backend APIs."""

from typing import Literal, TypeAlias

from pydantic import BaseModel
from typing_extensions import TypedDict

ModelType: TypeAlias = Literal["gemini-1.5-flash-001", "6894888983713546240"]


class TrialMetadataMeasureOutcomeType(TypedDict):
    measure: str
    description: str
    timeFrame: str


class TrialMetadataInterventionType(TypedDict):
    type: str
    name: str
    description: str


class TrialMetadataReferenceType(TypedDict):
    pmid: str
    citation: str


class TrialMetadataDocumentType(TypedDict):
    url: str
    size: int


class TrialMetadataType(TypedDict):
    shortTitle: str
    longTitle: str
    organization: str
    submitDate: str
    submitDateQc: str
    submitDatePosted: str
    resultsDate: str
    resultsDateQc: str
    resultsDatePosted: str
    lastUpdateDate: str
    lastUpdateDatePosted: str
    verifyDate: str
    sponsor: str
    collaborators: list[str]
    summary: str
    details: str
    conditions: list[str]
    studyPhases: str
    studyType: str
    enrollmentCount: int
    allocation: str
    interventionModel: str
    observationalModel: str
    primaryPurpose: str
    whoMasked: str
    interventions: list[TrialMetadataInterventionType]
    primaryMeasureOutcomes: list[TrialMetadataMeasureOutcomeType]
    secondaryMeasureOutcomes: list[TrialMetadataMeasureOutcomeType]
    otherMeasureOutcomes: list[TrialMetadataMeasureOutcomeType]
    minAge: int
    maxAge: int
    eligibleSex: str
    acceptsHealthy: bool
    inclusionCriteria: str
    exclusionCriteria: str
    officials: list[str]
    locations: list[str]
    references: list[TrialMetadataReferenceType]
    documents: list[TrialMetadataDocumentType]


class TrialFilters(TypedDict, total=False):
    studyType: str
    studyPhases: str
    minAge: int
    maxAge: int
    eligibleSex: str
    lastUpdateDate: str
    


class APIHeartbeatResponseType(TypedDict):
    timestamp: int


class APIRetrieveResponseType(TypedDict):
    ids: list[str]
    documents: list[str]


class APIMetaResponseType(TypedDict):
    metadata: TrialMetadataType


class APIChatPayloadType(BaseModel):
    query: str


class APIChatResponseType(TypedDict):
    response: str
