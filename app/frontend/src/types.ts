/**
 * @file types.ts
 *
 * This file defines custom types and interfaces for the application.
 */

/**
 * The appearance type.
 */
export type ApperanceType = "dark" | "light";

/**
 * The model type.
 */
export type ModelType = "gemini-1.5-flash-001" | "6894888983713546240";

/**
 * The type of a primary/secondary/other measure outcome of a clinical trial.
 */
export interface TrialMetadataMeasureOutcomeType {
  measure: string;
  description: string;
  timeFrame: string;
}

/**
 * The type of an intervention of a clinical trial.
 */
export interface TrialMetadataInterventionType {
  type: string;
  name: string;
  description: string;
}

/**
 * The type of a reference of a clinical trial.
 */
export interface TrialMetadataReferenceType {
  pmid: string;
  citation: string;
}

/**
 * The type of a document of a clinical trial.
 */
export interface TrialMetadataDocumentType {
  url: string;
  size: number;
}

/**
 * The type of metadata of a clinical trial.
 */
export interface TrialMetadataType {
  shortTitle: string;
  longTitle: string;
  organization: string;
  submitDate: string;
  submitDateQc: string;
  submitDatePosted: string;
  resultsDate: string;
  resultsDateQc: string;
  resultsDatePosted: string;
  lastUpdateDate: string;
  lastUpdateDatePosted: string;
  verifyDate: string;
  sponsor: string;
  collaborators: string[];
  summary: string;
  details: string;
  conditions: string[];
  studyPhases: string;
  studyType: string;
  enrollmentCount: number;
  allocation: string;
  interventionModel: string;
  observationalModel: string;
  primaryPurpose: string;
  whoMasked: string;
  interventions: TrialMetadataInterventionType[];
  primaryMeasureOutcomes: TrialMetadataMeasureOutcomeType[];
  secondaryMeasureOutcomes: TrialMetadataMeasureOutcomeType[];
  otherMeasureOutcomes: TrialMetadataMeasureOutcomeType[];
  minAge: number;
  maxAge: number;
  eligibleSex: string;
  acceptsHealthy: boolean;
  inclusionCriteria: string;
  exclusionCriteria: string;
  officials: string[];
  locations: string[];
  references: TrialMetadataReferenceType[];
  documents: TrialMetadataDocumentType[];
}

/**
 * The type to wrap an okay response from the API or an error message.
 */
export type WrapAPI<T> = { payload: T } | { error: string };

/**
 * The type of a response from the /heartbeat API endpoint.
 */
export interface APIHeartbeatResponseType {
  timestamp: number;
}

/**
 * The type of a response from the /retrieve API endpoint.
 */
export interface APIRetrieveResponseType {
  ids: string[];
  documents?: string[];
  metadata?: TrialMetadataType[];
}

/**
 * The type of a response from the /chat/{endpoint}/{item_id} API endpoint.
 */
export interface APIChatResponseType {
  response: string;
}
